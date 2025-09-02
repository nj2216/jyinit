# Supported Templates 🧩

- `library` – Python library scaffold
- `flask` – Flask web application
- `fastapi` – FastAPI application
- `django` – Django project scaffold
- `mlops` – MLOps project structure with training scripts
- `streamlit` – Streamlit app scaffold
- `aws-lambda` – AWS Lambda project scaffold
- `sanic`, `aiohttp` – Async Python web frameworks

> Run `python jyinit.py list-templates` to see the full list of bundled templates and licenses.

<details>
<summary>Tip: Multiple templates in one project</summary>

```bash
python jyinit.py create mycombo --types flask mlops streamlit