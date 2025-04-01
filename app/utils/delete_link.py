from datetime import datetime
from ..models.link import Link
from ..db.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_link_after_expiration(short_code: str, expires_at: datetime):
    if datetime.utcnow() >= expires_at:
        db = SessionLocal()
        db_link = db.query(Link).filter(Link.short_code == short_code).first()
        if db_link:
            db.delete(db_link)
            db.commit()
            logger.info(f"Deleted link with short code: {short_code} after expiration.")
        else:
            logger.warning(f"Link with short code: {short_code} not found for deletion.")