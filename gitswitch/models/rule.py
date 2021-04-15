from sqlalchemy import (
    Boolean,
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base

class Rule(Base):
    __tablename__ = 'rule'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    automerge = Column(Boolean)
    autorepair = Column(Boolean)
    
    from_branch_id = Column(ForeignKey('from_branch.id'), nullable=False)
    from_branch = relationship('Branch')
    to_branch_id = Column(ForeignKey('to_branch.id'), nullable=False)
    to_branch = relationship('Branch')
    via_branch_id = Column(ForeignKey('via_branch.id'), nullable=True)
    via_branch = relationship('Branch')
    