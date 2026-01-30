import requests
import re

REQUEST_TIMEOUT_SECONDS = 10


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
    """
    if not isinstance(gender, str) or not gender.strip():
        raise ValueError
    if not isinstance(has_work, bool):
        raise ValueError
    
    session = requests.Session()
    session.trust_env = False
    response = session.get(
        "https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json",
        timeout=REQUEST_TIMEOUT_SECONDS
    )
    response.raise_for_status()
    heroes = response.json()

    matching_heroes = []

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
        matching_heroes.append((height_cm, hero))

    if not matching_heroes:
        raise ValueError

    matching_heroes.sort(key=lambda x: x[0], reverse=True)
    return matching_heroes[0][1]
