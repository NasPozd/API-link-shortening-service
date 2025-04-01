import pytest
from app.routers.links import generate_unique_short_code

def test_short_code_uniqueness():
    existing_code = "abc123"
    new_code = generate_unique_short_code(existing_code)
    assert new_code != existing_code
    assert len(new_code) == 6

def test_short_code_generation_without_input():
    code = generate_unique_short_code(None)
    assert len(code) == 6
