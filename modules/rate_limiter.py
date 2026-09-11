import time
from collections import defaultdict
from threading import Lock


class RateLimiter:
    """
    Simple server-side, in-memory rate limiter.

    Tracks requests by a client identifier such as
    an email address, session identifier, or IP address.
    """

    def __init__(self, max_attempts=5, window_seconds=60):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds

        self._attempts = defaultdict(list)
        self._lock = Lock()

    def is_allowed(self, identifier):
        """
        Check whether another request is allowed.

        Returns:
            True  -> request is allowed
            False -> rate limit exceeded
        """

        if not identifier:
            return False

        identifier = str(identifier).strip().lower()

        current_time = time.time()

        with self._lock:

            timestamps = self._attempts[identifier]

            # Remove attempts outside the current window.
            timestamps[:] = [
                timestamp
                for timestamp in timestamps
                if current_time - timestamp < self.window_seconds
            ]

            if len(timestamps) >= self.max_attempts:
                return False

            timestamps.append(current_time)

            return True

    def get_remaining_attempts(self, identifier):
        """
        Return the number of requests remaining
        in the current rate-limit window.
        """

        if not identifier:
            return 0

        identifier = str(identifier).strip().lower()

        current_time = time.time()

        with self._lock:

            timestamps = self._attempts[identifier]

            timestamps[:] = [
                timestamp
                for timestamp in timestamps
                if current_time - timestamp < self.window_seconds
            ]

            remaining = self.max_attempts - len(timestamps)

            return max(0, remaining)

    def reset(self, identifier):
        """
        Reset the rate limit for an identifier.
        """

        if not identifier:
            return

        identifier = str(identifier).strip().lower()

        with self._lock:
            self._attempts.pop(identifier, None)


# Login protection.
login_rate_limiter = RateLimiter(
    max_attempts=5,
    window_seconds=60,
)


# AI request protection.
ai_rate_limiter = RateLimiter(
    max_attempts=10,
    window_seconds=60,
)


# Resume-processing protection.
resume_rate_limiter = RateLimiter(
    max_attempts=5,
    window_seconds=60,
)