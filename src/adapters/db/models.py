from sqlalchemy import Column, Integer, String, Boolean, DateTime
from . import Base


class S3Buckets(Base):
    __tablename__ = "s3_buckets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    was_default = Column(Boolean)
    last_updated = Column(DateTime, default=datetime.datetime.now)
