import pytest
from datetime import datetime
from app.schemas.link import LinkCreate
from pydantic import ValidationError


def test_link_create_validation():
    valid_data = {
        "original_url": "https://example.com",
        "expires_at": datetime.utcnow()
    }
    assert LinkCreate(**valid_data)

def test_invalid_url():
    with pytest.raises(ValidationError):
        LinkCreate(original_url="invalid_url", expires_at="...")