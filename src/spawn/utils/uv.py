import subprocess


def initialize_uv(project_path):
    try:
        subprocess.run(
            ["uv", "init", "--bare"],
            cwd=project_path,
            check=True,
        )

        subprocess.run(
            ["uv", "venv"],
            cwd=project_path,
            check=True,
        )

    except FileNotFoundError:
        raise RuntimeError(
            "UV is not installed."
        )