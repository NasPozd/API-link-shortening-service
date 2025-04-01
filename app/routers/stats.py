from fastapi import APIRouter, HTTPException
from ..models.link import Link
from ..db.database import SessionLocal
from ..models.link import Link

router = APIRouter()

@router.get("/links/{short_code}/stats")
def get_link_stats(short_code: str):
    db = SessionLocal()
    db_link = db.query(Link).filter(Link.short_code == short_code).first()
    if db_link:
        return {
            "original_url": db_link.original_url,
            "created_at": db_link.created_at,
            "clicks": db_link.clicks,
            "last_accessed": db_link.last_accessed
        }
    raise HTTPException(status_code=404, detail="Link not found")
