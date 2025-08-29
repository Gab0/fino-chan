#!/bin/python

import datetime
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv

import database
import image_management

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from openai import OpenAI


def read_env_file(file_path: str):
    """
    Read a .env file and load the environment variables.

    :param file_path: Path to the .env file
    """
    load_dotenv(file_path)


def get_image(message: str):
    response = client.images.generate(
      model="dall-e-3",
      prompt=f"Generate a modern painting about this: '{message[:970]}'",
      size="1024x1024",
      quality="standard",
      n=1,
    )

    image = response.data[0]

    return image


def get_transformed_count():
    session = Session()
    dt = datetime.datetime.now() - datetime.timedelta(hours=1)
    count = session.query(database.TransformedMessage).where(database.TransformedMessage.created_on > dt).count()
    session.close()
    return count


def translate_message(text, system_prompt):
    """Translate a message using OpenAI API."""
    response = client.chat.completions.create(
        model="o3",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ])
    return response.choices[0].message.content.strip()


def check_messages(max_number: int):
    print("Checking messages...")

    session = Session()
    messages = session.query(database.Message).filter(~database.Message.transformed_messages.any()).all()
    system_prompt = session.query(database.Prompt).all()[0]
    
    print(f"Found {len(messages)} messages to transform")
    
    for m in messages:
        print(m.message)
        print(m.transformed_messages)

        if m.transformed_messages:
            continue

        max_number -= 1
        if max_number < 0:
            print("Aborting checks.")
            break

        try:
            transformed_text = translate_message(m.message, system_prompt.body)
        except Exception as e:
            print("Error while transforming message: {e}")
            transformed_text = "🍷"
        print(transformed_text)
        tm = database.TransformedMessage(
            transformed_text=transformed_text,
            original_message_id=m.id,
            original_message=m
        )

        session.add(tm)
        session.commit()
        session.refresh(tm)

        print("Generating image...")

        if m.transformed_messages[0].message_images:
            continue

        try:
            generate_image(tm, session)
        except Exception as e:
            print(f"Error while generating image: {e}")

    session.close()


def generate_image(tm: database.TransformedMessage, session):
    image_id = str(uuid.uuid4())
    generated_image = get_image(tm.transformed_text)
    image = database.Image(
        url=generated_image.url,
        revised_prompt=generated_image.revised_prompt,
        image_id=image_id,
        transformed_message_id=tm.id
    )

    local_image_path = image_management.get_image_path(image_id)
    image_management.download_image(
        generated_image.url,
        local_image_path
    )

    image_management.upload_to_s3(
        str(local_image_path),
        "fino-chan"
    )

    session.add(image)
    session.commit()
    print("Done.")


if __name__ == "__main__":
    read_env_file(".env")
    MAX_MPH = 20
    client = OpenAI()
    Session = sessionmaker(bind=database.get_engine())
    while True:
        try:
            t_count = get_transformed_count()
            print(f"Transformed {t_count} messages in the past hour.")

            if t_count > MAX_MPH:
                print("Waiting...")
                time.sleep(20)
                continue

            check_messages(MAX_MPH - t_count)

        except Exception as e:
            raise e

        time.sleep(20)
