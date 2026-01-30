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


def assert_height_positive(hero, extract_height):
    height_cm = extract_height(hero)
    assert height_cm > 0
