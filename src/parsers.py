import re


def extract_height_cm(hero: dict) -> float:
    height_values = hero.get("appearance", {}).get("height", [])
    if not height_values or len(height_values) < 2:
        return 0.0
    height_cm_str = height_values[1]
    match = re.search(r"(\d+(?:\.\d+)?)", height_cm_str)
    if not match:
        return 0.0
    return float(match.group(1))
