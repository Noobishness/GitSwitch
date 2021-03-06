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

    repo_id = Column(ForeignKey('repo.id'), nullable=False)
    repo = relationship('Repo')