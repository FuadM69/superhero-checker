import os
import re
import sys

import pytest
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from hero import REQUEST_TIMEOUT_SECONDS, get_tallest_hero


class BaseTest:
    def call_get_tallest_hero(self, gender: str, has_work: bool):
        try:
            return get_tallest_hero(gender, has_work)
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Пропуск теста из-за сетевой ошибки: {type(e).__name__}: {str(e)}")

    def _fetch_all_heroes(self):
        session = requests.Session()
        session.trust_env = False
        try:
            response = session.get(
                "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json",
                timeout=REQUEST_TIMEOUT_SECONDS
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Пропуск теста из-за сетевой ошибки: {type(e).__name__}: {str(e)}")

    def get_max_height_among_matching(self, gender: str, has_work: bool) -> float:
        heroes = self._fetch_all_heroes()
        matching_heights = []
        for hero in heroes:
            hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
            if hero_gender != gender.strip().lower():
                continue
            work_occupation = hero.get("work", {}).get("occupation", "")
            has_occupation = work_occupation and work_occupation != "-"
            if has_work != has_occupation:
                continue
            height_str = hero.get("appearance", {}).get("height", [])
            if not height_str or len(height_str) < 2:
                continue
            height_cm_str = height_str[1]
            match = re.search(r"(\d+(?:\.\d+)?)", height_cm_str)
            if not match:
                continue
            height_cm = float(match.group(1))
            matching_heights.append(height_cm)
        if not matching_heights:
            raise ValueError
        return max(matching_heights)

    def extract_height_cm(self, hero: dict) -> float:
        height_str = hero.get("appearance", {}).get("height", [])
        if not height_str or len(height_str) < 2:
            return 0.0
        height_cm_str = height_str[1]
        match = re.search(r"(\d+(?:\.\d+)?)", height_cm_str)
        if not match:
            return 0.0
        return float(match.group(1))
