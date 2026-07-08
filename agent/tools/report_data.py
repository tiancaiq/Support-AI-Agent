import csv
import re


MONTH_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
USER_ID_PATTERN = re.compile(r"^\d+$")


def validate_user_id(user_id: str) -> str:
    cleaned = str(user_id).strip()
    if not USER_ID_PATTERN.fullmatch(cleaned):
        raise ValueError("user_id must be a numeric string")
    return cleaned


def validate_month(month: str) -> str:
    cleaned = str(month).strip()
    if not MONTH_PATTERN.fullmatch(cleaned):
        raise ValueError("month must use YYYY-MM format")
    return cleaned


def load_external_data(csv_path: str) -> dict[str, dict[str, dict[str, str]]]:
    records: dict[str, dict[str, dict[str, str]]] = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = validate_user_id(row["user_id"])
            month = validate_month(row["time"])
            records.setdefault(user_id, {})[month] = {
                "profile": row["profile"],
                "cleaning_efficiency": row["cleaning_efficiency"],
                "consumables": row["consumables"],
                "comparison": row["comparison"],
            }
    return records
