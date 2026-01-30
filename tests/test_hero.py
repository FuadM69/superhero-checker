import pytest

from .helpers import assert_gender, assert_has_work, assert_height_positive
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
    """Проверяет: мужской герой с занятием — пол, occupation и рост > 0."""
    hero = call_get_tallest_hero(GENDER_MALE, HAS_WORK_TRUE)
    assert isinstance(hero, dict)
    assert_gender(hero, GENDER_MALE)
    assert_has_work(hero, HAS_WORK_TRUE)
    assert_height_positive(hero, extract_height)


def test_female_without_work_gender_occupation_empty_height_positive(
    call_get_tallest_hero, extract_height
):
    """Проверяет: женский герой без занятия — пол, пустой occupation и рост > 0."""
    hero = call_get_tallest_hero(GENDER_FEMALE, HAS_WORK_FALSE)
    assert_gender(hero, GENDER_FEMALE)
    assert_has_work(hero, HAS_WORK_FALSE)
    assert_height_positive(hero, extract_height)


def test_gender_case_insensitive(call_get_tallest_hero, extract_height):
    """Проверяет: один и тот же герой при разном регистре пола (male / MALE)."""
    hero_lower = call_get_tallest_hero("male", HAS_WORK_TRUE)
    hero_upper = call_get_tallest_hero("MALE", HAS_WORK_TRUE)
    assert isinstance(hero_lower, dict) and isinstance(hero_upper, dict)
    assert hero_lower.get("id") == hero_upper.get("id")
    assert_height_positive(hero_lower, extract_height)
    assert_height_positive(hero_upper, extract_height)


@pytest.mark.parametrize("gender", ["", 123, None])
def test_invalid_gender_raises_value_error(call_get_tallest_hero, gender):
    """Проверяет: невалидный или пустой gender вызывает ValueError."""
    with pytest.raises(ValueError):
        call_get_tallest_hero(gender, HAS_WORK_TRUE)


@pytest.mark.parametrize("has_work", [1, "yes"])
def test_invalid_has_work_raises_value_error(call_get_tallest_hero, has_work):
    """Проверяет: не bool для has_work вызывает ValueError."""
    with pytest.raises(ValueError):
        call_get_tallest_hero(GENDER_MALE, has_work)


def test_gender_no_matches_raises_value_error(call_get_tallest_hero):
    """Проверяет: пол без совпадений в API вызывает ValueError."""
    with pytest.raises(ValueError):
        call_get_tallest_hero(GENDER_NO_MATCH, HAS_WORK_TRUE)


def test_returned_hero_is_tallest_among_matching(
    call_get_tallest_hero, extract_height, get_max_height_among_matching
):
    """Проверяет: возвращённый герой — самый высокий среди подходящих."""
    hero = call_get_tallest_hero(GENDER_MALE, HAS_WORK_TRUE)
    max_height = get_max_height_among_matching(GENDER_MALE, HAS_WORK_TRUE)
    returned_height = extract_height(hero)
    assert returned_height == max_height
