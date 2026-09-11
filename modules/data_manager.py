import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json_file(filename):
    """
    Load a JSON data file from the project's data directory.
    """
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_careers():
    """
    Load career information.
    """
    return load_json_file("careers.json")


def load_skills():
    """
    Load skill information.
    """
    return load_json_file("skills.json")


def load_projects():
    """
    Load project recommendation data.
    """
    return load_json_file("projects.json")


def load_career_profiles():
    """
    Load the career profile dataset.
    """
    file_path = DATA_DIR / "career_profiles.csv"

    return pd.read_csv(file_path)


def get_dataset_summary():
    """
    Return a summary of the career profile dataset.
    """
    dataframe = load_career_profiles()

    return {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": list(dataframe.columns),
    }


def get_data_summary():
    """
    Return a summary of all major project data sources.
    """
    careers = load_careers()
    skills = load_skills()
    projects = load_projects()
    profiles = load_career_profiles()

    return {
        "careers_count": len(careers),
        "skills_count": len(skills),
        "projects_count": len(projects),
        "career_profiles_count": len(profiles),
        "career_profiles_columns": len(profiles.columns),
    }