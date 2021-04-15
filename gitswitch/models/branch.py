from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base

class Branch(Base):
    __tablename__ = 'branch'
    id = Column(Integer, primary_key=True)
    name = Column(Text)