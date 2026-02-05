import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.constants import BASE_URL, HEROES_ENDPOINT
from src.http import get


@pytest.fixture(scope="session")
def all_heroes():
    response = get(f"{BASE_URL}{HEROES_ENDPOINT}")
    response.raise_for_status()
    return response.json()
