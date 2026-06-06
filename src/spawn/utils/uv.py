import subprocess
from pathlib import Path

from spawn.core.exceptions import SpawnError


def initialize_uv(project_path: Path) -> None:
    try:
        subprocess.run(
            ["uv", "init", "--bare"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )

        subprocess.run(
            ["uv", "venv"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True,
        )

    except FileNotFoundError:
        raise SpawnError(
            "UV is not installed or not available in PATH."
        )

    except subprocess.CalledProcessError:
        raise SpawnError(
            "Failed to initialize UV environment."
        )