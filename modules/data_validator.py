import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def validate_json_file(filename):
    """
    Validate that a JSON file exists and contains valid JSON.
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return False, f"{filename} not found."

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            json.load(file)

        return True, f"{filename} is valid."

    except json.JSONDecodeError:
        return False, f"{filename} contains invalid JSON."

    except Exception as error:
        return False, f"{filename} could not be read: {error}"


def validate_csv_file(filename):
    """
    Validate that a CSV file exists and can be loaded.
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return False, f"{filename} not found."

    try:
        dataframe = pd.read_csv(file_path)

        if dataframe.empty:
            return False, f"{filename} is empty."

        return True, (
            f"{filename} is valid with "
            f"{len(dataframe)} rows and {len(dataframe.columns)} columns."
        )

    except Exception as error:
        return False, f"{filename} could not be read: {error}"


def validate_project_data():
    """
    Validate all major project data files.
    """
    results = {}

    json_files = [
        "careers.json",
        "skills.json",
        "projects.json",
    ]

    for filename in json_files:
        valid, message = validate_json_file(filename)
        results[filename] = {
            "valid": valid,
            "message": message,
        }

    valid, message = validate_csv_file("career_profiles.csv")

    results["career_profiles.csv"] = {
        "valid": valid,
        "message": message,
    }

    return results


def all_data_valid():
    """
    Return True only when all project data files are valid.
    """
    results = validate_project_data()

    return all(item["valid"] for item in results.values())