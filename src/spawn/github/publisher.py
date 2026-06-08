from pathlib import Path

from spawn.github.validators import (
    is_valid_github_url,
)
from spawn.github.exceptions import (
    GitHubPublishError,
)


class GitHubPublisher:
    def publish(
        self,
        project_path: Path,
        repo_url: str,
    ) -> None:

        if not project_path.exists():
            raise GitHubPublishError(
                f"Project path does not exist: {project_path}"
            )

        if not is_valid_github_url(repo_url):
            raise GitHubPublishError(
                "Invalid GitHub repository URL."
            )

        # Publishing workflow arrives in Sprint 2