import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


DATASET_PATH = "data/career_profiles.csv"


def load_dataset():
    df = pd.read_csv(DATASET_PATH)

    df = df.dropna(
        subset=["current_job_title", "top_skills"]
    )

    return df


def map_career(job_title):
    title = job_title.lower()

    if "software engineer" in title:
        return "Software Developer"

    if "ml engineer" in title:
        return "Machine Learning Engineer"

    if "data analyst" in title:
        return "Data Analyst"

    if "cloud engineer" in title:
        return "Cloud Engineer"

    return None


def train_model():

    df = load_dataset()

    df["career"] = df["current_job_title"].apply(
        map_career
    )

    df = df.dropna(
        subset=["career"]
    )

    X = df["top_skills"].astype(str)
    y = df["career"]

    vectorizer = TfidfVectorizer(
        token_pattern=r"[^;]+"
    )

    X_vectorized = vectorizer.fit_transform(X)

    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(
        X_vectorized,
        y
    )

    return model, vectorizer


def predict_top_careers(user_skills, top_n=3):

    model, vectorizer = train_model()

    skills_text = ";".join(
        user_skills
    )

    skills_vectorized = vectorizer.transform(
        [skills_text]
    )

    probabilities = model.predict_proba(
        skills_vectorized
    )[0]

    classes = model.classes_

    ranked_indices = probabilities.argsort()[::-1]

    results = []

    for index in ranked_indices[:top_n]:

        results.append({
            "career": classes[index],
            "confidence": round(
                probabilities[index] * 100,
                2
            )
        })

    return results


def predict_career(user_skills):

    results = predict_top_careers(
        user_skills,
        top_n=1
    )

    return (
        results[0]["career"],
        results[0]["confidence"]
    )