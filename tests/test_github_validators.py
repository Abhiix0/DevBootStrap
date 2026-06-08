from spawn.github.validators import (
    is_valid_github_url,
)


def test_valid_https_url():
    assert is_valid_github_url(
        "https://github.com/user/repo"
    )


def test_valid_https_git_url():
    assert is_valid_github_url(
        "https://github.com/user/repo.git"
    )


def test_valid_ssh_url():
    assert is_valid_github_url(
        "git@github.com:user/repo.git"
    )


def test_empty_url():
    assert not is_valid_github_url("")


def test_invalid_url():
    assert not is_valid_github_url(
        "hello world"
    )


def test_non_github_url():
    assert not is_valid_github_url(
        "https://google.com"
    )