import pytest
from app.main import app
from fastapi.testclient import TestClient
from app.db.database import Base, engine

@pytest.fixture(scope="session")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def mock_cache(mocker):
    mocker.patch("app.utils.cache.get_cache", return_value=None)
    mocker.patch("app.utils.cache.set_cache")
    
@pytest.fixture(autouse=True)
def cleanup_db():
    yield
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)