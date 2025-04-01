import pytest
from app.models.user import User as UserModel
from app.core.security import hash_password, verify_password

def test_user_creation():
    user = UserModel(username="testuser", hashed_password=hash_password("testpass"))
    assert user.username == "testuser"
    assert verify_password("testpass", user.hashed_password)

def test_password_hashing():
    password = "secure123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)