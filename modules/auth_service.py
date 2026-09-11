from modules.authentication import (
    hash_password,
    verify_password,
)
from modules.database import (
    create_user,
    create_user_profile,
    get_user_by_email,
    update_last_login,
)
from modules.rate_limiter import login_rate_limiter
from modules.security_monitor import (
    log_login_failure,
    log_login_rate_limited,
    log_login_success,
    log_registration,
)


def normalize_email(email):
    """
    Normalize an email address before storing or searching.
    """
    if not isinstance(email, str):
        return ""

    return email.strip().lower()


def validate_email(email):
    """
    Perform basic email validation.
    """
    email = normalize_email(email)

    if not email:
        return False

    if len(email) > 254:
        return False

    if "@" not in email:
        return False

    local_part, domain = email.rsplit("@", 1)

    if not local_part or not domain:
        return False

    if "." not in domain:
        return False

    return True


def validate_password(password):
    """
    Validate password requirements.

    Password policy:
    - At least 8 characters
    - At most 128 characters
    """
    if not isinstance(password, str):
        return False

    if len(password) < 8:
        return False

    if len(password) > 128:
        return False

    return True


def register_user(email, password):
    """
    Register a new user securely.

    Returns:
        {
            "success": bool,
            "message": str,
            "user": dict | None
        }
    """
    email = normalize_email(email)

    if not validate_email(email):
        return {
            "success": False,
            "message": "Please enter a valid email address.",
            "user": None,
        }

    if not validate_password(password):
        return {
            "success": False,
            "message": (
                "Password must contain between "
                "8 and 128 characters."
            ),
            "user": None,
        }

    existing_user = get_user_by_email(email)

    if existing_user is not None:
        return {
            "success": False,
            "message": "An account with this email already exists.",
            "user": None,
        }

    password_hash = hash_password(password)

    user_id = create_user(
        email=email,
        password_hash=password_hash,
    )

    if user_id is None:
        return {
            "success": False,
            "message": "Unable to create the account.",
            "user": None,
        }

    create_user_profile(user_id)

    user = get_user_by_email(email)

    log_registration(email)

    return {
        "success": True,
        "message": "Account created successfully.",
        "user": user,
    }


def login_user(email, password):
    """
    Authenticate a user securely with server-side rate limiting
    and security monitoring.

    Returns:
        {
            "success": bool,
            "message": str,
            "user": dict | None
        }
    """
    email = normalize_email(email)

    if not email or not isinstance(password, str):
        log_login_failure(email)

        return {
            "success": False,
            "message": "Invalid email or password.",
            "user": None,
        }

    if not login_rate_limiter.is_allowed(email):
        log_login_rate_limited(email)

        return {
            "success": False,
            "message": (
                "Too many login attempts. "
                "Please try again later."
            ),
            "user": None,
        }

    user = get_user_by_email(email)

    if user is None:
        log_login_failure(email)

        return {
            "success": False,
            "message": "Invalid email or password.",
            "user": None,
        }

    password_hash = user.get("password_hash")

    if not verify_password(password, password_hash):
        log_login_failure(email)

        return {
            "success": False,
            "message": "Invalid email or password.",
            "user": None,
        }

    login_rate_limiter.reset(email)

    update_last_login(user["id"])

    user = get_user_by_email(email)

    log_login_success(email)

    return {
        "success": True,
        "message": "Login successful.",
        "user": user,
    }