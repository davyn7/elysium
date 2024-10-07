import asyncio

from app.configs.secrets import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from app.db.client import DBClient

# Create an instance of DBClient and create database connections
db_client = DBClient(
    user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME
)

db_client.create_database_connection()
db_client.create_async_database_connection()

# TODO: incorporate this into db_client and set the semaphore config into yaml and getter
db_semaphore = asyncio.Semaphore(10)