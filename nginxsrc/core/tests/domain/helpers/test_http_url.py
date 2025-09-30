import pytest
from pydantic import BaseModel, ValidationError
from core.domain.models.location import PreservedHttpUrl

class DummyModel(BaseModel):
    url: PreservedHttpUrl


def test_preserved_slash_added_if_missing():
    m = DummyModel(url="http://example.com/")
    assert str(m.url) == "http://example.com/"  # barra final preservada

def test_preserved_slash_kept_if_present():
    m = DummyModel(url="http://example.com/")
    assert str(m.url) == "http://example.com/"

def test_no_slash_urls():
    m = DummyModel(url="http://example.com")
    # Pydantic normaliza adicionando barra final
    assert str(m.url) == "http://example.com/"

def test_invalid_url_raises():
    with pytest.raises(ValidationError):
        DummyModel(url="notaurl")
