import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "security.log"


def _get_logger():
    """
    Create and configure the security logger.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("career_platform_security")

    if not logger.handlers:
        handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.setLevel(logging.INFO)

        logger.propagate = False

    return logger


def _safe_identifier(identifier):
    """
    Convert an identifier into a safe value for logging.

    Sensitive information such as passwords, resume text,
    API keys, and authentication tokens must never be logged.
    """

    if identifier is None:
        return "unknown"

    identifier = str(identifier).strip()

    if not identifier:
        return "unknown"

    # Prevent newlines from being inserted into log entries.
    identifier = (
        identifier
        .replace("\r", "")
        .replace("\n", "")
    )

    # Avoid excessively large log entries.
    return identifier[:254]


def log_event(event, identifier=None):
    """
    Record a general security event.
    """

    logger = _get_logger()

    safe_event = _safe_identifier(event)
    safe_identifier = _safe_identifier(identifier)

    logger.info(
        "event=%s | identifier=%s",
        safe_event,
        safe_identifier,
    )


def log_login_success(identifier):
    """
    Record a successful login.
    """

    log_event(
        "login_success",
        identifier,
    )


def log_login_failure(identifier):
    """
    Record a failed login attempt.
    """

    log_event(
        "login_failure",
        identifier,
    )


def log_login_rate_limited(identifier):
    """
    Record a login request blocked by rate limiting.
    """

    log_event(
        "login_rate_limited",
        identifier,
    )


def log_ai_rate_limited(identifier):
    """
    Record an AI request blocked by rate limiting.
    """

    log_event(
        "ai_rate_limited",
        identifier,
    )


def log_resume_rate_limited(identifier):
    """
    Record a resume-processing request blocked
    by rate limiting.
    """

    log_event(
        "resume_rate_limited",
        identifier,
    )


def log_registration(identifier):
    """
    Record a successful account registration.
    """

    log_event(
        "registration_success",
        identifier,
    )


def log_logout(identifier):
    """
    Record a user logout event.
    """

    log_event(
        "logout",
        identifier,
    )


def log_security_error(identifier, error_type):
    """
    Record a security-related error without storing
    sensitive error details.
    """

    log_event(
        f"security_error:{error_type}",
        identifier,
    )


def get_log_file():
    """
    Return the security log file path.
    """

    _get_logger()

    return LOG_FILE