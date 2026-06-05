import subprocess


def initialize_git(project_path):
    try:
        subprocess.run(
            ["git", "init"],
            cwd=project_path,
            check=True,
        )

    except FileNotFoundError:
        raise RuntimeError(
            "Git is not installed."
        )