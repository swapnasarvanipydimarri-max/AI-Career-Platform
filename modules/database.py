import json
import sqlite3
from pathlib import Path

from modules.encryption import encrypt_text, decrypt_text


# Project database location
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "career_platform.db"


def get_connection():
    """
    Create a connection to the SQLite database.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign-key enforcement.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def _encrypt_optional(value):
    """
    Encrypt a value when it contains data.
    """
    if value is None:
        return ""

    value = str(value)

    if not value:
        return ""

    return encrypt_text(value)


def _decrypt_optional(value):
    """
    Decrypt a value when it contains encrypted data.
    """
    if value is None:
        return ""

    value = str(value)

    if not value:
        return ""

    return decrypt_text(value)


def initialize_database():
    """
    Create all required database tables if they do not exist.
    """
    connection = get_connection()

    cursor = connection.cursor()

    # User authentication table.
    #
    # Email is kept as a normalized identifier so the application
    # can locate the account during login.
    #
    # Passwords are never stored directly.
    # Only the Argon2id password hash is stored.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT
        )
        """
    )

    # User profile table.
    #
    # Sensitive profile fields are stored encrypted.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            name TEXT DEFAULT '',
            education TEXT DEFAULT '',
            experience_years REAL,
            skills TEXT DEFAULT '',
            career_interests TEXT DEFAULT '',
            resume_text TEXT DEFAULT '',
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # Career analysis history.
    #
    # analysis_data may contain career information derived from
    # the user's resume/profile, so it is encrypted before storage.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS career_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            analysis_data TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # Add resume_text to databases created by the previous version.
    _add_column_if_missing(
        connection,
        "user_profiles",
        "resume_text",
        "TEXT DEFAULT ''",
    )

    connection.commit()
    connection.close()


def _add_column_if_missing(
    connection,
    table_name,
    column_name,
    column_definition,
):
    """
    Add a database column when it does not already exist.
    """
    cursor = connection.cursor()

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = {
        row["name"]
        for row in cursor.fetchall()
    }

    if column_name not in columns:
        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_definition}
            """
        )


def create_user(email, password_hash):
    """
    Create a new user.

    Returns:
        User ID if successful.
        None if the email already exists.
    """
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                email,
                password_hash
            )
            VALUES (?, ?)
            """,
            (
                email.strip().lower(),
                password_hash,
            ),
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None

    finally:
        connection.close()


def get_user_by_email(email):
    """
    Retrieve a user by email address.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            email,
            password_hash,
            created_at,
            last_login
        FROM users
        WHERE email = ?
        """,
        (email.strip().lower(),),
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    return dict(user)


def update_last_login(user_id):
    """
    Update the user's last login timestamp.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET last_login = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (user_id,),
    )

    connection.commit()
    connection.close()


def create_user_profile(user_id):
    """
    Create an empty profile for a user if one does not exist.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO user_profiles (
            user_id
        )
        VALUES (?)
        """,
        (user_id,),
    )

    connection.commit()
    connection.close()


def get_user_profile(user_id):
    """
    Retrieve and decrypt a user's profile.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            user_id,
            name,
            education,
            experience_years,
            skills,
            career_interests,
            resume_text
        FROM user_profiles
        WHERE user_id = ?
        """,
        (user_id,),
    )

    profile = cursor.fetchone()

    connection.close()

    if profile is None:
        return None

    profile = dict(profile)

    return {
        "user_id": profile["user_id"],
        "name": _decrypt_optional(profile["name"]),
        "education": _decrypt_optional(
            profile["education"]
        ),
        "experience_years": profile[
            "experience_years"
        ],
        "skills": _decrypt_json(
            profile["skills"]
        ),
        "career_interests": _decrypt_json(
            profile["career_interests"]
        ),
        "resume_text": _decrypt_optional(
            profile["resume_text"]
        ),
    }


def _encrypt_json(value):
    """
    Convert a Python value to JSON and encrypt it.
    """
    if value is None:
        value = []

    json_value = json.dumps(
        value,
        ensure_ascii=False,
    )

    return encrypt_text(json_value)


def _decrypt_json(value):
    """
    Decrypt a JSON value and convert it back to Python.
    """
    if value is None or not str(value):
        return []

    decrypted = decrypt_text(str(value))

    try:
        result = json.loads(decrypted)

    except json.JSONDecodeError as error:
        raise ValueError(
            "Stored profile data is not valid JSON."
        ) from error

    return result


def update_user_profile(
    user_id,
    name="",
    education="",
    experience_years=None,
    skills=None,
    career_interests=None,
    resume_text="",
):
    """
    Encrypt and update a user's profile information.
    """
    if skills is None:
        skills = []

    if career_interests is None:
        career_interests = []

    encrypted_name = _encrypt_optional(name)
    encrypted_education = _encrypt_optional(
        education
    )
    encrypted_skills = _encrypt_json(skills)
    encrypted_interests = _encrypt_json(
        career_interests
    )
    encrypted_resume = _encrypt_optional(
        resume_text
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO user_profiles (
            user_id,
            name,
            education,
            experience_years,
            skills,
            career_interests,
            resume_text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(user_id)
        DO UPDATE SET
            name = excluded.name,
            education = excluded.education,
            experience_years = excluded.experience_years,
            skills = excluded.skills,
            career_interests = excluded.career_interests,
            resume_text = excluded.resume_text
        """,
        (
            user_id,
            encrypted_name,
            encrypted_education,
            experience_years,
            encrypted_skills,
            encrypted_interests,
            encrypted_resume,
        ),
    )

    connection.commit()
    connection.close()


def save_career_analysis(user_id, analysis_data):
    """
    Encrypt and save a career-analysis result.
    """
    if not isinstance(analysis_data, str):
        analysis_data = json.dumps(
            analysis_data,
            ensure_ascii=False,
        )

    encrypted_analysis = encrypt_text(
        analysis_data
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO career_analyses (
            user_id,
            analysis_data
        )
        VALUES (?, ?)
        """,
        (
            user_id,
            encrypted_analysis,
        ),
    )

    connection.commit()

    analysis_id = cursor.lastrowid

    connection.close()

    return analysis_id


def get_career_analysis_history(user_id, limit=20):
    """
    Retrieve and decrypt recent career analyses.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            analysis_data,
            created_at
        FROM career_analyses
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (
            user_id,
            int(limit),
        ),
    )

    analyses = cursor.fetchall()

    connection.close()

    results = []

    for analysis in analyses:
        analysis = dict(analysis)

        results.append(
            {
                "id": analysis["id"],
                "analysis_data": _decrypt_optional(
                    analysis["analysis_data"]
                ),
                "created_at": analysis["created_at"],
            }
        )

    return results


def delete_user_data(user_id):
    """
    Delete all stored data associated with a user.
    """
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM career_analyses
        WHERE user_id = ?
        """,
        (user_id,),
    )

    cursor.execute(
        """
        DELETE FROM user_profiles
        WHERE user_id = ?
        """,
        (user_id,),
    )

    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,),
    )

    connection.commit()
    connection.close()