from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from sqlalchemy import create_engine, inspect
from app.models.base import Base
import logging
from sqlalchemy.exc import OperationalError
from app.core.config import DATABASE_URL

DATABASE_URL = DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        logger.info("Initializing the database...")
        
        inspector = inspect(engine)
        if not inspector.has_table("links") or not inspector.has_table("users"):
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully.")
        else:
            logger.warning("Tables already exist. Skipping creation.")
            
    except OperationalError as e:
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise