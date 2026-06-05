from rich.panel import Panel

from spawn.utils.console import console


def show_next_steps(project_name: str, template: str) -> None:
    commands = {
        "python": [
            f"cd {project_name}",
            "uv run python main.py",
        ],
        "fastapi": [
            f"cd {project_name}",
            "uv add fastapi uvicorn",
            "uv run uvicorn app.main:app --reload",
        ],
        "data-science": [
            f"cd {project_name}",
            "uv add pandas numpy matplotlib",
        ],
        "ml": [
            f"cd {project_name}",
            "uv add pandas numpy scikit-learn",
        ],
    }

    steps = commands.get(template, [])

    content = "\n".join(steps)

    console.print(
        Panel(
            content,
            title="🚀 Next Steps",
            border_style="green",
        )
    )