from src.constants import BASE_URL, HEROES_ENDPOINT
from src.http import get
from src.parsers import extract_height_cm


def get_tallest_hero(gender: str, has_work: bool) -> dict:
    """
    Возвращает самого высокого героя, соответствующего критериям.

    Args:
        gender: Пол героя (сравнение без учета регистра и пробелов).
        has_work: Если True, герой должен иметь непустое занятие (work.occupation),
                  если False, герой не должен иметь занятия (null/пустое/"-").

    Returns:
        dict: Полный JSON словарь самого высокого подходящего героя.

    Raises:
        ValueError: Если ни один герой не соответствует критериям.
        requests.HTTPError: При ошибке HTTP (например, от raise_for_status()).
    """
    if not isinstance(gender, str) or not gender.strip():
        raise ValueError
    if not isinstance(has_work, bool):
        raise ValueError

    response = get(f"{BASE_URL}{HEROES_ENDPOINT}")
    response.raise_for_status()
    heroes = response.json()

    max_height = 0.0
    best_hero = None

    for hero in heroes:
        hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
        if hero_gender != gender.strip().lower():
            continue

        work_occupation = hero.get("work", {}).get("occupation", "")
        has_occupation = work_occupation and work_occupation != "-"

        if has_work != has_occupation:
            continue

        height_cm = extract_height_cm(hero)
        if height_cm <= 0:
            continue

        if height_cm > max_height:
            max_height = height_cm
            best_hero = hero

    if best_hero is None:
        raise ValueError

    return best_hero
