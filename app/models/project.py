from ..models.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    links = relationship("Link", back_populates="project")
