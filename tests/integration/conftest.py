from os import environ, system

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.core.database import get_url
from app.core.models.base import Base


@fixture(scope="session", autouse=True)
def setup():
    environ["POSTGRES_DB"] = "cash-flow"
    postgres_container = PostgresContainer("postgres:12.2-alpine")
    with postgres_container as postgres:
        environ["DATABASE_URL"] = postgres.get_connection_url()
        engine = create_engine(get_url())
        system("alembic upgrade head")
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        yield Session


@fixture(scope="function")
def db(setup):
    session = setup()
    yield session
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()
