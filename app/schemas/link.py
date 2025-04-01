from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional
from datetime import datetime

class LinkCreate(BaseModel):
    user_id: Optional[int] = None
    original_url: str
    custom_alias: Optional[str] = None 
    expires_at: Optional[datetime] = None

class LinkUpdate(BaseModel):
    original_url: str

class LinkStats(BaseModel):
    original_url: str
    created_at: datetime
    clicks: int
    last_accessed: Optional[datetime] = None

class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    clicks: int
    last_accessed: Optional[datetime] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
