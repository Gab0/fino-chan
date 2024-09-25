import database

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=database.get_engine())
session = Session()

messages = session.query(database.Message).all()

for m in messages:
    print(m.message)
    print(m.transformed_messages)

    tm = database.TransformedMessage(
        transformed_text="111",
        original_message_id=m.id,
        original_message=m
    )

    session.add(tm)
    session.commit()
