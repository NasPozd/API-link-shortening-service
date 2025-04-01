from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse
from ..models.link import Link
from ..utils.short_code import generate_unique_short_code
from ..utils.valid_url import is_valid_url
from ..utils.delete_link import delete_link_after_expiration
from ..models.user import User as UserModel
from datetime import datetime, timedelta
from ..schemas.link import LinkCreate, LinkResponse
from ..db.database import SessionLocal
from ..core.security import get_current_user
from ..utils.cache import set_cache, get_cache
import logging


router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/links/", response_model=LinkResponse)
def create_link(link: LinkCreate, background_tasks: BackgroundTasks, current_user: UserModel = Depends(get_current_user)):
    if not link.original_url:
        logger.error("Original URL is required.")
        raise HTTPException(status_code=400, detail="Original URL is required.")
    
    if not is_valid_url(link.original_url):
        logger.error("Invalid URL format.")
        raise HTTPException(status_code=422, detail="Invalid URL format.")
    
    if not link.custom_alias and not link.original_url:
        logger.error("Either a custom alias or original URL must be provided.")
        raise HTTPException(status_code=400, detail="Either a custom alias or original URL must be provided.")
    
    logger.info(f"Received request to create link: {link}")
    db = SessionLocal()
    
    existing_link = db.query(Link).filter(Link.short_code == link.custom_alias).first()
    if existing_link:
        link.custom_alias = generate_unique_short_code(link.custom_alias)
    elif not link.custom_alias:
        link.custom_alias = generate_unique_short_code(None)  
    
    try:
        db_link = Link(original_url=link.original_url, short_code=link.custom_alias, expires_at=link.expires_at, user_id=current_user.id if current_user else None, last_accessed=datetime.utcnow())
        db.add(db_link)
        db.commit()
        db.refresh(db_link)

        if link.expires_at:
            background_tasks.add_task(delete_link_after_expiration, db_link.short_code, link.expires_at)

        logger.info(f"Link creation successful: {db_link}, original URL: {db_link.original_url}, short code: {db_link.short_code}, created at: {db_link.created_at}, user ID: {db_link.user_id}")
        return LinkResponse(
            id=db_link.id,
            original_url=db_link.original_url,
            short_code=db_link.short_code,
            created_at=db_link.created_at,
            expires_at=db_link.expires_at,
            clicks=db_link.clicks,
            last_accessed=db_link.last_accessed,
            user_id=db_link.user_id
        )
    except Exception as e:
        logger.error(f"An error occurred during link creation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/links/search")
def search_link(original_url: str = Query(...)):
    db = SessionLocal()
    db_link = db.query(Link).filter(Link.original_url == original_url).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    return LinkResponse.model_validate(db_link)

@router.get("/links/expired", response_model=list[LinkResponse])
def get_expired_links():
    db = SessionLocal()
    expired_links = db.query(Link).filter(Link.expires_at < datetime.utcnow()).all()
    return [LinkResponse.model_validate(link) for link in expired_links]

@router.delete("/links/unused", response_model=list[LinkResponse])
def delete_unused_links(days: int = 30):
    db = SessionLocal()  
    threshold_date = datetime.utcnow() - timedelta(days=days)  
    unused_links = db.query(Link).filter(Link.last_accessed < threshold_date).all()  
    
    for link in unused_links:  
        db.delete(link)  
    db.commit()  
    
    return [LinkResponse.model_validate(link) for link in unused_links]

@router.put("/links/{short_code}", response_model=LinkResponse)
def update_link(short_code: str, link: LinkCreate, current_user: UserModel = Depends(get_current_user)) -> LinkResponse:
    db = SessionLocal()
    db_link = db.query(Link).filter(Link.short_code == short_code).first()
    
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db_link.original_url = link.original_url
    if link.expires_at:
        db_link.expires_at = link.expires_at
    
    db.commit()
    db.refresh(db_link)
    
    return LinkResponse.model_validate(db_link)

@router.delete("/links/{short_code}", status_code=204)
def delete_link(short_code: str, current_user: UserModel = Depends(get_current_user)):
    db = SessionLocal()
    db_link = db.query(Link).filter(Link.short_code == short_code).first()
    
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db.delete(db_link)
    db.commit()
    
    return

@router.get("/links/{short_code}")
def redirect_link(short_code: str):
    try:
        logger.info(f"Attempting to redirect for short code: {short_code}.")
        cached_url = get_cache(short_code)
        
        if cached_url:
            return RedirectResponse(url=cached_url.decode('utf-8'))

        db = SessionLocal()
        db_link = db.query(Link).filter(Link.short_code == short_code).first()
        if db_link is None:
            raise HTTPException(status_code=404, detail="Link not found")
        
        db_link.clicks += 1
        db_link.last_accessed = datetime.utcnow()
        db.commit()
        
        set_cache(short_code, db_link.original_url)
        return RedirectResponse(url=db_link.original_url, status_code=302)
    except Exception as e:
        logger.error(f"Error during redirect: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
