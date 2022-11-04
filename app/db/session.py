from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config.setting import settings


def get_db_uri():
    return (f'{settings.DB_TYPE}://{settings.MARIA_DB_USER}:%s@'
            f'{settings.MARIA_DB_SERVER}/{settings.MARIA_DB}?charset=utf8' % quote(settings.MARIA_DB_PASSWORD))


SQLALCHEMY_DATABASE_URI = get_db_uri()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
