import os
import sys

import pytest
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.constants import BASE_URL, HEROES_ENDPOINT
from src.hero import get_tallest_hero
from src.http import get
from src.parsers import extract_height_cm


@pytest.fixture
def call_get_tallest_hero():
    def _call(gender, has_work):
        try:
            return get_tallest_hero(gender, has_work)
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Пропуск теста из-за сетевой ошибки: {type(e).__name__}: {str(e)}")

    return _call


@pytest.fixture
def extract_height():
    return extract_height_cm


@pytest.fixture(scope="session")
def all_heroes():
    try:
        response = get(f"{BASE_URL}{HEROES_ENDPOINT}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Пропуск теста из-за сетевой ошибки: {type(e).__name__}: {str(e)}")


def _matches(hero, gender, has_work):
    hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
    if hero_gender != gender.strip().lower():
        return False
    work_occupation = hero.get("work", {}).get("occupation", "")
    has_occupation = work_occupation and work_occupation != "-"
    return has_work == has_occupation


@pytest.fixture
def get_max_height_among_matching(all_heroes, extract_height):
    def _get_max(gender, has_work):
        matching_heights = []
        for hero in all_heroes:
            if not _matches(hero, gender, has_work):
                continue
            height_cm = extract_height(hero)
            if height_cm <= 0:
                continue
            matching_heights.append(height_cm)
        if not matching_heights:
            raise ValueError
        return max(matching_heights)

    return _get_max
