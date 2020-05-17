from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DEFAULT_DATABASE_URL = "postgresql://postgres:postgres@localhost/cash-flow"


def get_url():
    return getenv("DATABASE_URL", default=DEFAULT_DATABASE_URL,)


engine = create_engine(get_url())
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        session = Session()
        yield session
        session.commit()
    except Exception as error:
        session.rollback()
        raise error
    finally:
        session.close()
