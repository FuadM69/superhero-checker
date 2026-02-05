from src.parsers import extract_height_cm


def assert_gender(hero, expected_gender):
    hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
    assert hero_gender == expected_gender.strip().lower()


def assert_has_work(hero, expected_has_work):
    work = hero.get("work")
    work_occupation = work.get("occupation") if work is not None else None
    if expected_has_work:
        assert work_occupation and work_occupation != "-"
    else:
        assert work_occupation in (None, "", "-")


def assert_height_positive(hero, extract_height=extract_height_cm):
    height_cm = extract_height(hero)
    assert height_cm > 0


def matches(hero, gender, has_work):
    """True if hero matches gender and has_work criteria."""
    hero_gender = hero.get("appearance", {}).get("gender", "").strip().lower()
    if hero_gender != gender.strip().lower():
        return False
    work_occupation = hero.get("work", {}).get("occupation", "")
    has_occupation = work_occupation and work_occupation != "-"
    return has_work == has_occupation


def get_reference_max_height(all_heroes, gender, has_work):
    """Among heroes matching gender and has_work, return the maximum height in cm."""
    max_height = 0.0
    for hero in all_heroes:
        if not matches(hero, gender, has_work):
            continue
        height_cm = extract_height_cm(hero)
        if height_cm <= 0:
            continue
        if height_cm > max_height:
            max_height = height_cm
    if max_height == 0.0:
        raise ValueError("No matching heroes with valid height")
    return max_height
