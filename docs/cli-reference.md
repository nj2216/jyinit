# CLI Reference 📋

| Option | Description |
|--------|-------------|
| `--types <template1> <template2>` | One or more templates to scaffold. |
| `--dir` | Directory in which to create the project (default: current directory). |
| `--license` | License to include (default: MIT). |
| `--author` | Author name to embed in license file. |
| `--py` | Minimum Python version (default: 3.8). |
| `--git` | Initialize git repository for each subproject (no remote). |
| `--gitrep [url]` | Initialize git for each subproject and optionally set a remote URL. |
| `--venv` | Create a `.venv` virtual environment for each subproject. |
| `--no-tests` | Skip creating a `tests/` folder. |
| `--ci` | Add GitHub Actions workflow (`.github/workflows/python-package.yml`). |
| `--interactive` | Prompt for missing values interactively. |
| `--dry-run` | Preview actions without creating files or running commands. |

<details>
<summary>Legacy option</summary>

- `--type` – legacy single template option, use `--types` instead.

</details>