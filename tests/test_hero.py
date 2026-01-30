import pytest

from .testdata.constants import (
    GENDER_FEMALE,
    GENDER_MALE,
    GENDER_NO_MATCH,
    HAS_WORK_FALSE,
    HAS_WORK_TRUE,
)


def test_male_with_work_returns_hero_gender_occupation_height_positive(
    call_get_tallest_hero, extract_height
):
    hero = call_get_tallest_hero(GENDER_MALE, HAS_WORK_TRUE)
    assert isinstance(hero, dict)
    hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
    assert hero_gender == GENDER_MALE.strip().lower()
    work_occupation = hero.get("work", {}).get("occupation", "")
    assert work_occupation and work_occupation != "-"
    height_cm = extract_height(hero)
    assert height_cm > 0


def test_female_without_work_gender_occupation_empty_height_positive(
    call_get_tallest_hero, extract_height
):
    hero = call_get_tallest_hero(GENDER_FEMALE, HAS_WORK_FALSE)
    hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
    assert hero_gender == GENDER_FEMALE.strip().lower()
    work = hero.get("work")
    work_occupation = work.get("occupation") if work is not None else None
    assert work_occupation in (None, "", "-")
    height_cm = extract_height(hero)
    assert height_cm > 0


def test_gender_case_insensitive(call_get_tallest_hero, extract_height):
    hero_lower = call_get_tallest_hero("male", HAS_WORK_TRUE)
    hero_upper = call_get_tallest_hero("MALE", HAS_WORK_TRUE)
    assert isinstance(hero_lower, dict) and isinstance(hero_upper, dict)
    assert hero_lower.get("id") == hero_upper.get("id")
    height_lower = extract_height(hero_lower)
    height_upper = extract_height(hero_upper)
    assert height_lower > 0 and height_upper > 0


@pytest.mark.parametrize("gender", ["", 123, None])
def test_invalid_gender_raises_value_error(call_get_tallest_hero, gender):
    with pytest.raises(ValueError):
        call_get_tallest_hero(gender, HAS_WORK_TRUE)


@pytest.mark.parametrize("has_work", [1, "yes"])
def test_invalid_has_work_raises_value_error(call_get_tallest_hero, has_work):
    with pytest.raises(ValueError):
        call_get_tallest_hero(GENDER_MALE, has_work)


def test_gender_no_matches_raises_value_error(call_get_tallest_hero):
    with pytest.raises(ValueError):
        call_get_tallest_hero(GENDER_NO_MATCH, HAS_WORK_TRUE)


def test_returned_hero_is_tallest_among_matching(
    call_get_tallest_hero, extract_height, get_max_height_among_matching
):
    hero = call_get_tallest_hero(GENDER_MALE, HAS_WORK_TRUE)
    max_height = get_max_height_among_matching(GENDER_MALE, HAS_WORK_TRUE)
    returned_height = extract_height(hero)
    assert returned_height == max_height
