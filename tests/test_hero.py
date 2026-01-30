import pytest

from .base_test import BaseTest
from .testdata.constants import (
    GENDER_FEMALE,
    GENDER_MALE,
    GENDER_NO_MATCH,
    HAS_WORK_FALSE,
    HAS_WORK_TRUE,
)


class TestGetTallestHero(BaseTest):
    def test_male_with_work_returns_hero_gender_occupation_height_positive(self):
        hero = self.call_get_tallest_hero(GENDER_MALE, HAS_WORK_TRUE)
        assert isinstance(hero, dict)
        hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
        assert hero_gender == GENDER_MALE.strip().lower()
        work_occupation = hero.get("work", {}).get("occupation", "")
        assert work_occupation and work_occupation != "-"
        height_cm = self.extract_height_cm(hero)
        assert height_cm > 0

    def test_female_without_work_gender_occupation_empty_height_positive(self):
        hero = self.call_get_tallest_hero(GENDER_FEMALE, HAS_WORK_FALSE)
        hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
        assert hero_gender == GENDER_FEMALE.strip().lower()
        work = hero.get("work")
        work_occupation = work.get("occupation") if work is not None else None
        assert work_occupation in (None, "", "-")
        height_cm = self.extract_height_cm(hero)
        assert height_cm > 0

    def test_gender_case_insensitive(self):
        hero_lower = self.call_get_tallest_hero("male", HAS_WORK_TRUE)
        hero_upper = self.call_get_tallest_hero("MALE", HAS_WORK_TRUE)
        assert isinstance(hero_lower, dict) and isinstance(hero_upper, dict)
        assert hero_lower.get("id") == hero_upper.get("id")
        height_lower = self.extract_height_cm(hero_lower)
        height_upper = self.extract_height_cm(hero_upper)
        assert height_lower > 0 and height_upper > 0

    def test_invalid_gender_type_or_empty_raises_value_error(self):
        with pytest.raises(ValueError):
            self.call_get_tallest_hero("", HAS_WORK_TRUE)
        with pytest.raises(ValueError):
            self.call_get_tallest_hero(123, HAS_WORK_TRUE)
        with pytest.raises(ValueError):
            self.call_get_tallest_hero(None, HAS_WORK_TRUE)

    def test_has_work_not_bool_raises_value_error(self):
        with pytest.raises(ValueError):
            self.call_get_tallest_hero(GENDER_MALE, 1)
        with pytest.raises(ValueError):
            self.call_get_tallest_hero(GENDER_MALE, "yes")

    def test_gender_no_matches_raises_value_error(self):
        with pytest.raises(ValueError):
            self.call_get_tallest_hero(GENDER_NO_MATCH, HAS_WORK_TRUE)

    def test_returned_hero_is_tallest_among_matching(self):
        hero = self.call_get_tallest_hero(GENDER_MALE, HAS_WORK_TRUE)
        max_height = self.get_max_height_among_matching(GENDER_MALE, HAS_WORK_TRUE)
        returned_height = self.extract_height_cm(hero)
        assert returned_height == max_height
