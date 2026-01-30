import re


def extract_height_cm(hero: dict) -> float:
    height_str = hero.get("appearance", {}).get("height", [])
    if not height_str or len(height_str) < 2:
        return 0.0
    height_cm_str = height_str[1]
    match = re.search(r"(\d+(?:\.\d+)?)", height_cm_str)
    if not match:
        return 0.0
    return float(match.group(1))
