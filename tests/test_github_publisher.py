from pathlib import Path

import pytest

from spawn.github.publisher import (
    GitHubPublisher,
)
from spawn.github.exceptions import (
    GitHubPublishError,
)


def test_missing_project_path():
    publisher = GitHubPublisher()

    with pytest.raises(
        GitHubPublishError
    ):
        publisher.publish(
            Path("missing"),
            "https://github.com/user/repo",
        )


def test_invalid_repo_url(tmp_path):
    publisher = GitHubPublisher()

    with pytest.raises(
        GitHubPublishError
    ):
        publisher.publish(
            tmp_path,
            "not-a-url",
        )