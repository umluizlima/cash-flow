from app.core.database import get_url, DEFAULT_DATABASE_URL


def test_get_url_returns_from_environment(monkeypatch):
    expected = "some_database_url"
    monkeypatch.setenv("DATABASE_URL", expected)

    received = get_url()

    assert received == expected


def test_get_url_returns_default_value(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    received = get_url()

    assert received == DEFAULT_DATABASE_URL
