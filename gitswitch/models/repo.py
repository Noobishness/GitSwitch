from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base

class Repo(Base):
    __tablename__ = 'repo'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    remote_path = Column(Text)
    local_path = Column(Text)
    username = Column(Text)
    token = Column(Text)
