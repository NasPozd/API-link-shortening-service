from app.db.database import SessionLocal
from app.models.link import Link

def test_link_lifecycle():
    db = SessionLocal()
    link = Link(original_url="http://test.com", short_code="test123")
    db.add(link)
    db.commit()
    
    retrieved = db.query(Link).filter_by(short_code="test123").first()
    assert retrieved is not None
    
    db.delete(retrieved)
    db.commit()
    assert db.query(Link).filter_by(short_code="test123").first() is None