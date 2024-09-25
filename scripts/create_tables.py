
from sqlalchemy.schema import CreateTable

import database


if __name__ == "__main__":

    # Create an engine (replace with your actual database URL)
    engine = database.get_engine()

    # Generate CREATE TABLE statements
    metadata = database.Base.metadata
    tables = [database.Message.__table__, database.TransformedMessage.__table__]

    for table in tables:
        print(CreateTable(table).compile(engine))

    # Execute the CREATE TABLE statements
    database.Base.metadata.create_all(engine)
    print("Tables created successfully.")



