from ..models.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.database import Base

class Link(Base):
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    clicks = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    def is_expired(self) -> bool:
        return self.expires_at is not None and datetime.utcnow() >= self.expires_at