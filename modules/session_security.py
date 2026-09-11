import secrets
import time


# Session timeout after 30 minutes of inactivity.
SESSION_TIMEOUT_SECONDS = 30 * 60


def create_session(user_id):
    """
    Create a secure application session.
    """

    if user_id is None:
        raise ValueError("user_id is required.")

    return {
        "session_id": secrets.token_urlsafe(32),
        "user_id": user_id,
        "created_at": time.time(),
        "last_activity": time.time(),
    }


def is_session_valid(session):
    """
    Check whether a session exists and has not expired.
    """

    if not isinstance(session, dict):
        return False

    required_fields = {
        "session_id",
        "user_id",
        "created_at",
        "last_activity",
    }

    if not required_fields.issubset(session):
        return False

    if not session["session_id"]:
        return False

    if session["user_id"] is None:
        return False

    current_time = time.time()

    last_activity = session["last_activity"]

    if current_time - last_activity > SESSION_TIMEOUT_SECONDS:
        return False

    return True


def refresh_session(session):
    """
    Refresh the session activity timestamp.
    """

    if not is_session_valid(session):
        return None

    session["last_activity"] = time.time()

    return session


def destroy_session(session):
    """
    Securely invalidate a session.
    """

    if not isinstance(session, dict):
        return

    session.clear()


def get_session_id(session):
    """
    Return the current session identifier.
    """

    if not is_session_valid(session):
        return None

    return session["session_id"]