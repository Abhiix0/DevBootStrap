# Architecture

## 1. Overview

Spawn is a Python CLI tool built with Typer and Rich. It scaffolds new Python projects from templates, optionally publishes them to GitHub, and scores existing projects for environment health.

The three main capabilities are **project generation** (`spawn create`), **GitHub publishing** (optional post-create flow), and **environment health checking** (`spawn doctor`).

## 2. Technology Stack

| Tool | Version | Role |
|---|---|---|
| Python | 3.12+ | Core language |
| Typer | 0.26.7+ | CLI framework |
| Rich | 15.0.0+ | Terminal UI |
| uv | any | Environment management |
| Git | any | Version control |
| Hatchling | any | Build backend |

Entry point: `spawn.cli.app:main` (defined in `pyproject.toml` as `[project.scripts]`).

## 3. Repository Structure

```
src/spawn/
├── __init__.py         # __version__ lookup via importlib.metadata
├── cli/
│   ├── app.py          # Typer app, command definitions (create, version, doctor)
│   └── prompts.py      # Interactive prompt logic, TEMPLATE_CHOICES mapping
├── core/
│   ├── exceptions.py   # SpawnError — base exception for all Spawn errors
│   ├── models.py       # ProjectConfig dataclass
│   └── registry.py     # Template registry, get_template() lookup
├── generators/
│   └── project_generator.py  # Orchestrates folder creation, file writing, git+uv init
├── github/
│   ├── exceptions.py   # GitHubPublishError
│   ├── publisher.py    # GitHubPublisher — stages, commits, pushes
│   └── validators.py   # GitHub URL validation (regex)
├── templates/
│   ├── base.py         # BaseTemplate dataclass (name, folders, starter_files)
│   ├── files.py        # README_CONTENT and GITIGNORE_CONTENT strings
│   ├── python_script.py
│   ├── fastapi.py
│   ├── data_science.py
│   └── ml_project.py
└── utils/
    ├── console.py      # Shared Rich Console instance
    ├── doctor.py       # ProjectHealthChecker, HealthCheck dataclass, run_health_check()
    ├── git.py          # initialize_git(), run_git_command(), add_all(), commit(), push etc.
    ├── next_steps.py   # Template-specific next steps commands
    ├── success.py      # show_success() — renders the success panel
    ├── uv.py           # initialize_uv() — runs uv init --bare and uv venv
    └── validators.py   # validate_project_name() — regex validation
```

`templates/files.py` also holds starter-file content constants (`PYTHON_MAIN_CONTENT`, `FASTAPI_MAIN_CONTENT`, etc.) used by individual template modules.

## 4. Key Flows

### 4a. Project Creation Flow

1. User runs `spawn create`
2. `app.create()` prints the opening Rich panel
3. `get_project_config()` collects name, template, and Git preference via Typer/Rich prompts
4. `ProjectGenerator.generate()` resolves the template, creates the directory, writes files, and runs `initialize_git()` (if enabled) and `initialize_uv()`
5. `show_success()` renders the success panel with template-specific next steps from `show_next_steps()`
6. If Git was enabled, `Confirm.ask("Publish to GitHub?")` runs; on yes, `GitHubPublisher.publish()` stages, commits, and pushes

```
spawn create
    │
    ▼
get_project_config()          prompts.py
    │  → ProjectConfig
    ▼
ProjectGenerator.generate()   project_generator.py
    ├── get_template()        registry.py
    ├── mkdir + write files   templates/
    ├── initialize_git()      git.py          (if use_git)
    └── initialize_uv()       uv.py
    │
    ▼
show_success()                success.py
    └── show_next_steps()     next_steps.py
    │
    ▼
GitHubPublisher.publish()     publisher.py    (optional)
    └── git add / commit / push
```

### 4b. Template System

`BaseTemplate` is a dataclass with three fields:

| Field | Type | Purpose |
|---|---|---|
| `name` | `str` | Display name shown in the success panel |
| `folders` | `list[str]` | Directories created under the project root |
| `starter_files` | `list[tuple[str, str]]` | `(relative_path, content_template)` pairs; `{project_name}` is substituted at write time |

Each template subclasses `BaseTemplate` in its own file under `templates/`:

| Class | Registry key |
|---|---|
| `PythonScriptTemplate` | `"python"` |
| `FastAPITemplate` | `"fastapi"` |
| `DataScienceTemplate` | `"data-science"` |
| `MLProjectTemplate` | `"ml"` |

`registry.py` holds the `TEMPLATES` dict mapping string keys to template classes. `get_template(template_name)` instantiates the class and returns it, or returns `None` if the key is missing.

`ProjectGenerator` always writes `README.md` and `.gitignore` from `files.py` regardless of template; template-specific files come from `starter_files`.

### 4c. Error Handling

Two-level exception hierarchy:

```
SpawnError                    # core/exceptions.py
└── GitHubPublishError        # github/exceptions.py
```

| Exception | Raised by | Caught in |
|---|---|---|
| `SpawnError` | `validators.py`, `project_generator.py`, `git.py`, `uv.py` | `app.create()` — generation step |
| `GitHubPublishError` | `publisher.py` (wraps `SpawnError` from git subprocess calls) | `app.create()` — publish step |

Subprocess failures in `git.py` and `uv.py` raise `SpawnError` with the stderr message or a fallback string. `ProjectGenerator.generate()` wraps its body in a try/except that calls `shutil.rmtree()` on any failure, so a partial directory is never left behind.

The CLI catches both exception types and prints `❌ {message}` in red via Rich — no traceback is shown to the user.

## 5. Adding a New Template

1. Create `src/spawn/templates/your_template.py` — subclass `BaseTemplate`, define `name`, `folders`, and `starter_files`
2. Register in `src/spawn/core/registry.py` — add your class to the `TEMPLATES` dict with a string key
3. Add next steps in `src/spawn/utils/next_steps.py` — add an entry to the `commands` dict keyed by your registry key
4. Add prompt row in `src/spawn/cli/prompts.py` — add to `TEMPLATE_CHOICES` and `table.add_row()` in the Rich table
5. Write tests — add to `tests/test_templates.py` and `tests/test_registry.py`

## 6. Running Tests

```bash
uv run pytest
```

```bash
uv run pytest -v
```

```bash
uv run pytest tests/test_doctor.py
```

```bash
uv run ruff check .
```
