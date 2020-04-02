import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def db_init():
    engine = create_engine(
        os.getenv("DB_URL")
    )

    from .models import S3Buckets

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session
