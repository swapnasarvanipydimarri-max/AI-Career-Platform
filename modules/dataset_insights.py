import pandas as pd


DATASET_PATH = "data/career_profiles.csv"


def load_career_dataset():
    """
    Load the career profile dataset.
    """

    df = pd.read_csv(DATASET_PATH)

    return df


def get_dataset_summary():
    """
    Return basic statistics about the career dataset.
    """

    df = load_career_dataset()

    total_profiles = len(df)

    total_columns = len(df.columns)

    return {
        "total_profiles": total_profiles,
        "total_columns": total_columns
    }


def get_career_distribution():
    """
    Get the distribution of job titles in the dataset.
    """

    df = load_career_dataset()

    distribution = (
        df["current_job_title"]
        .value_counts()
        .head(10)
    )

    return distribution


def get_top_skills():
    """
    Extract the most common skills from the dataset.
    """

    df = load_career_dataset()

    skill_counts = {}

    for skills in df["top_skills"].dropna():

        skills_list = str(skills).split(";")

        for skill in skills_list:

            skill = skill.strip()

            if skill:

                skill_counts[skill] = (
                    skill_counts.get(skill, 0) + 1
                )

    top_skills = sorted(
        skill_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return top_skills[:10]