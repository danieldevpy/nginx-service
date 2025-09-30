import pytest
from pydantic import ValidationError
from core.domain.models.location import Location, LocationType


# -------------------------
# Casos de sucesso
# -------------------------
def test_create_proxy_location_success():
    loc = Location(
        path="/",
        type=LocationType.PROXY,
        proxy_pass="http://127.0.0.1:3000"
    )
    assert loc.type == LocationType.PROXY
    assert str(loc.proxy_pass) == "http://127.0.0.1:3000/"


def test_create_redirect_location_success():
    loc = Location(
        path="/old",
        type=LocationType.REDIRECT,
        redirect_to="https://example.com/new",
        status_code=301
    )
    assert loc.type == LocationType.REDIRECT
    # Se redirect_to é PreservedHttpUrl, converta para string
    assert str(loc.redirect_to) == "https://example.com/new"
    assert loc.status_code == 301


def test_create_static_location_success():
    loc = Location(
        path="/static",
        type=LocationType.STATIC,
        root="/var/www/static"
    )
    assert loc.type == LocationType.STATIC
    assert loc.root == "/var/www/static"


def test_create_rewrite_location_success():
    loc = Location(
        path="/blog",
        type=LocationType.REWRITE,
        rewrite_rule="^/blog/(.*)$ /news/$1"
    )
    assert loc.type == LocationType.REWRITE
    assert loc.rewrite_rule.startswith("^/blog")


# -------------------------
# Casos de falha
# -------------------------
def test_proxy_missing_proxy_pass():
    with pytest.raises(ValidationError) as exc:
        Location(
            path="/",
            type=LocationType.PROXY
        )
    assert "proxy_pass" in str(exc.value)


def test_redirect_missing_fields():
    with pytest.raises(ValidationError) as exc:
        Location(
            path="/old",
            type=LocationType.REDIRECT
        )
    msg = str(exc.value)
    assert "redirect_to" in msg
    assert "status_code" in msg


def test_static_missing_root():
    with pytest.raises(ValidationError) as exc:
        Location(
            path="/static",
            type=LocationType.STATIC
        )
    assert "root" in str(exc.value)


def test_rewrite_missing_rule():
    with pytest.raises(ValidationError) as exc:
        Location(
            path="/blog",
            type=LocationType.REWRITE
        )
    assert "rewrite_rule" in str(exc.value)


# -------------------------
# Casos adicionais
# -------------------------
def test_invalid_type_string_rejected():
    with pytest.raises(ValidationError) as exc:
        Location(
            path="/",
            type="invalid",  # não permitido
            proxy_pass="http://127.0.0.1:3000"
        )
    msg = str(exc.value)
    # verificar parte da mensagem que não muda
    assert "Input should" in msg
    assert "type=enum" in msg
    # opcional: verificar que lista os valores válidos
    assert "proxy" in msg
    assert "redirect" in msg
    assert "static" in msg
    assert "rewrite" in msg


def test_extra_fields_are_allowed_if_not_required():
    # Proxy pode receber também 'status_code' mas não deve dar erro
    loc = Location(
        path="/",
        type=LocationType.PROXY,
        proxy_pass="http://127.0.0.1:3000",
        status_code=404
    )
    assert str(loc.proxy_pass) == "http://127.0.0.1:3000/"
    assert loc.status_code == 404
