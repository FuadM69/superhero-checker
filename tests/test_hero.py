import pytest

from src.hero import get_tallest_hero
from src.parsers import extract_height_cm
from tests.helpers import (
    assert_gender,
    assert_has_work,
    assert_height_positive,
    get_reference_max_height,
)
from tests.testdata.constants import (
    GENDER_FEMALE,
    GENDER_MALE,
    GENDER_NO_MATCH,
    HAS_WORK_FALSE,
    HAS_WORK_TRUE,
)


def test_male_with_work_returns_hero_gender_occupation_height_positive():
    """Проверяет: мужской герой с занятием — пол, occupation и рост > 0."""
    hero = get_tallest_hero(GENDER_MALE, HAS_WORK_TRUE)
    assert isinstance(hero, dict)
    assert_gender(hero, GENDER_MALE)
    assert_has_work(hero, HAS_WORK_TRUE)
    assert_height_positive(hero)


def test_female_without_work_gender_occupation_empty_height_positive():
    """Проверяет: женский герой без занятия — пол, пустой occupation и рост > 0."""
    hero = get_tallest_hero(GENDER_FEMALE, HAS_WORK_FALSE)
    assert_gender(hero, GENDER_FEMALE)
    assert_has_work(hero, HAS_WORK_FALSE)
    assert_height_positive(hero)


def test_gender_case_insensitive():
    """Проверяет: один и тот же герой при разном регистре пола (male / MALE)."""
    hero_lower = get_tallest_hero("male", HAS_WORK_TRUE)
    hero_upper = get_tallest_hero("MALE", HAS_WORK_TRUE)
    assert isinstance(hero_lower, dict) and isinstance(hero_upper, dict)
    assert hero_lower.get("id") == hero_upper.get("id")
    assert_height_positive(hero_lower)
    assert_height_positive(hero_upper)


@pytest.mark.parametrize("gender", ["", 123, None])
def test_invalid_gender_raises_value_error(gender):
    """Проверяет: невалидный или пустой gender вызывает ValueError."""
    with pytest.raises(ValueError):
        get_tallest_hero(gender, HAS_WORK_TRUE)


@pytest.mark.parametrize("has_work", [1, "yes"])
def test_invalid_has_work_raises_value_error(has_work):
    """Проверяет: не bool для has_work вызывает ValueError."""
    with pytest.raises(ValueError):
        get_tallest_hero(GENDER_MALE, has_work)


def test_gender_no_matches_raises_value_error():
    """Проверяет: пол без совпадений в API вызывает ValueError."""
    with pytest.raises(ValueError):
        get_tallest_hero(GENDER_NO_MATCH, HAS_WORK_TRUE)


@pytest.mark.parametrize(
    "gender,has_work",
    [
        (GENDER_MALE, HAS_WORK_TRUE),
        (GENDER_FEMALE, HAS_WORK_FALSE),
        (GENDER_FEMALE, HAS_WORK_TRUE),
        (GENDER_MALE, HAS_WORK_FALSE),
    ],
)
def test_returned_hero_is_tallest_among_matching(all_heroes, gender, has_work):
    """Возвращённый герой — самый высокий среди подходящих по полу и has_work."""
    hero = get_tallest_hero(gender, has_work)
    reference_max_height = get_reference_max_height(all_heroes, gender, has_work)
    assert extract_height_cm(hero) == reference_max_height
