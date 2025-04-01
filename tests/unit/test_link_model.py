from app.models.link import Link
from datetime import datetime, timedelta

def test_link_expiration():
    expires = datetime.utcnow() + timedelta(days=1)
    link = Link(original_url="https://example.com", short_code="abc123", expires_at=expires)
    assert not link.is_expired()
    
    link.expires_at = datetime.utcnow() - timedelta(minutes=1)
    assert link.is_expired()