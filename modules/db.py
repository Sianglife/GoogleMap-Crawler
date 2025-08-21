import os
from loguru import logger
from pymongo import MongoClient

URI = os.getenv("MONGO_URI")

client = MongoClient(URI)

db = None


def set_db(database_name):
    global db
    db = client[database_name]
    logger.info(f"Database set to: {database_name}")


def get_db():
    if db is None:
        raise ValueError("Database not set. Please call set_db() first.")
    return db


def db_insert(doc, collection):
    if db is None:
        raise ValueError("Database not set. Please call set_db() first.")
    return db[collection].insert_one(doc)


def db_find(query, collection):
    if db is None:
        raise ValueError("Database not set. Please call set_db() first.")
    return db[collection].find_one(query)


if __name__ == "__main__":
    print(URI)
