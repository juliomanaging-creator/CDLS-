import pytest

@pytest.fixture
def mock_db_connection():
    yield "mock_conn"

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test_token"}
