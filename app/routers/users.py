from fastapi import APIRouter, HTTPException
from ..models.user import User as UserModel
from ..schemas.user import UserCreate, UserLogin
from ..core.security import hash_password, verify_password
from ..db.database import SessionLocal
import jwt
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    logger.info(f"Received request to create user: {user}")  # Log the incoming request data
    db = SessionLocal()
    
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        logger.error("Username already taken")  # Log the error
        raise HTTPException(status_code=400, detail="Username already taken")
    
    db_user = UserModel(username=user.username, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created successfully: {db_user.username}")  # Log successful creation
    return UserCreate(username=db_user.username, password=user.password)

@router.post("/users/login")
def login(user: UserLogin):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required.")
    
    logger.info(f"User login attempt for username: {user.username}")  # Log the login attempt
    db = SessionLocal()
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logger.error(f"Invalid credentials for user: {user.username}")  # Log the error
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    logger.info(f"User logged in successfully: {user.username}")  # Log successful login
    from app.core.config import SECRET_KEY  # Importing SECRET_KEY
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm="HS256")  # Using imported SECRET_KEY
    return {"access_token": token, "token_type": "bearer"}
