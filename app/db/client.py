from sqlalchemy import schema
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session as SQLModelSession
from sqlmodel import SQLModel, create_engine


class DBClient:
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: int,
        database: str,
        is_github_action: bool = False,
    ):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.url_sync = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        self.url_async = (
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
        )
        self.is_github_action = is_github_action
        self.sync_engine = None
        self.async_engine = None
        self.get_sync_session = None
        self.get_async_session = None

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.sync_engine)

    def get_session(self) -> SQLModelSession:
        return SQLModelSession(self.sync_engine)

    def create_schema(self, schema_name: str):
        with self.sync_engine.connect() as connection:
            if schema_name not in connection.dialect.get_schema_names(connection):
                connection.execute(schema.CreateSchema(schema_name))
            connection.commit()
        SQLModel.metadata.create_all(self.sync_engine)

    def create_database_connection(self):
        if not self.is_github_action:
            self.sync_engine = create_engine(self.url_sync)
            self.get_sync_session = sessionmaker(bind=self.sync_engine)

    def create_async_database_connection(self):
        self.async_engine = create_async_engine(
            self.url_async, future=True, pool_size=50, max_overflow=60
        )
        self.get_async_session = sessionmaker(
            self.async_engine, class_=AsyncSession, expire_on_commit=False
        )