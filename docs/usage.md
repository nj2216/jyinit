# Usage 🛠️

### Create a New Project

**Single-template project:**

```bash
python jyinit.py create myproj --types library
````

**Interactive mode (prompts for missing values):**

```bash
python jyinit.py create myproj --interactive
```

**Flask app with CI and remote git repository:**

```bash
python jyinit.py create myrepo --types flask --ci --gitrep https://github.com/you/myrepo.git
```

**Multi-template project with virtual environments:**

```bash
python jyinit.py create combo --types streamlit mlops --venv --gitrep
```

### List Available Templates and Licenses

```bash
python jyinit.py list-templates
```

Preview actions without creating files:

```bash
python jyinit.py create demo --types flask --dry-run
```
