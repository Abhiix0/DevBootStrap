import re


_GITHUB_PATTERNS = (
    r"^https://github\.com/[\w.-]+/[\w.-]+/?$",
    r"^https://github\.com/[\w.-]+/[\w.-]+\.git$",
    r"^git@github\.com:[\w.-]+/[\w.-]+\.git$",
)


def is_valid_github_url(url: str) -> bool:
    """
    Validate supported GitHub repository URLs.
    """
    url = url.strip()

    if not url:
        return False

    return any(
        re.match(pattern, url)
        for pattern in _GITHUB_PATTERNS
    )