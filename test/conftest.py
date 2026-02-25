import pytest
from app.limiter import limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    limiter._storage.reset()
    yield
