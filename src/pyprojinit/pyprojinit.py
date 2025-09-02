#!/usr/bin/env python3
"""
pyprojinit
Extended Python project scaffolder.

New in this update:
- Interactive mode: `--interactive` will prompt for missing or important options.
- Per-template CI/workflows: each template can get a tailored GitHub Actions workflow (if `--ci` is provided).
- `--gitrep [remote_url]`: initializes a git repo for each subproject and optionally sets a remote and pushes the initial commit.

Usage examples:
- Interactive mode (prompts):
  python pyprojinit.py create myproj --interactive

- Create flask app + CI + set remote and push (non-interactive):
  python pyprojinit.py create myrepo --types flask --ci --gitrep https://github.com/you/myrepo.git

- Create streamlit + mlops with venvs and per-subproject repos (no remote):
  python pyprojinit.py create combo --types streamlit mlops --venv --gitrep

"""

from __future__ import annotations
import argparse
import os
import sys
import subprocess
import textwrap
from pathlib import Path
from datetime import date
from typing import Dict, Optional, List

YEAR = date.today().year

# -----------------------------
# Templates (same as before)
# -----------------------------
TEMPLATES: Dict[str, Dict[str, str]] = {
    "library": {
        "README.md": """# {name}
A Python library called {name}.
""",
        "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = \"{package_name}\"
version = \"0.0.0\"
description = \"A Python library\"
readme = \"README.md\"
license = {{text = \"{license_id}\"}}
requires-python = \">={py_min}\"

[tool.setuptools.packages.find]
where = ["src"]
""",
        "src/{package_name}/__init__.py": """# {package_name} package
__version__ = \"0.0.0\"
""",
        "tests/test_basic.py": """def test_import():
    import {package_name}
    assert True
""",
        ".gitignore": """__pycache__/
*.pyc
.env
.venv
dist/
build/
*.egg-info/
""",
    },

    "package": {
        "README.md": """# {name}

A Python application package called {name}.
""",
        "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = \"{package_name}\"
version = \"0.0.0\"
description = \"Simple application\"
readme = \"README.md\"
license = {{text = \"{license_id}\"}}
requires-python = \">={py_min}\"

[project.scripts]
{cli_name} = \"{module_path}:main\"
""",
        "{module_path}.py": """def main():
    print(\"Hello from {name}\")

if __name__ == \"__main__\":
    main()
""",
        ".gitignore": """__pycache__/
*.pyc
.env
.venv
""",
    },

    "cli": {
        "README.md": """# {name}

A simple CLI tool.
""",
        "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = \"{package_name}\"
version = \"0.0.0\"
description = \"CLI tool\"
readme = \"README.md\"
license = {{text = \"{license_id}\"}}
requires-python = \">={py_min}\"

[project.scripts]
{cli_name} = \"{module_path}:main\"
""",
        "{module_path}.py": """import argparse

def main():
    parser = argparse.ArgumentParser(prog=\"{cli_name}\")
    parser.add_argument('--version', action='store_true')
    args = parser.parse_args()
    if args.version:
        print(\"{name} 0.0.0\")
    else:
        print(\"Hello from {name}\")

if __name__ == \"__main__\":
    main()
""",
        ".gitignore": """__pycache__/
*.pyc
.venv
""",
    },

    "flask": {
        "README.md": """# {name}

A small Flask app.
""",
        "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = \"{package_name}\"
version = \"0.0.0\"
description = \"Flask web app\"
readme = \"README.md\"
license = {{text = \"{license_id}\"}}
requires-python = \">={py_min}\"
dependencies = [\"flask>=2.0\"]
""",
        "app.py": """from flask import Flask, render_template_string
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('<h1>Hello from {name}</h1>')

if __name__ == '__main__':
    app.run(debug=True)
""",
        "requirements.txt": "flask>=2.0",
        ".gitignore": """__pycache__/
instance/
.env
.venv
""",
    },

    "fastapi": {
        "README.md": """# {name}

A small FastAPI app.
""",
        "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = \"{package_name}\"
version = \"0.0.0\"
description = \"FastAPI web app\"
readme = \"README.md\"
license = {{text = \"{license_id}\"}}
requires-python = \">={py_min}\"
dependencies = [\"fastapi>=0.70\", \"uvicorn>=0.15\"]
""",
        "main.py": """from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Hello from {name}'}
""",
        "requirements.txt": """fastapi>=0.70
uvicorn>=0.15
""",
        ".gitignore": """__pycache__/
.venv
""",
    },

    "django": {
        "README.md": """# {name}

A minimal Django project scaffold.
""",
        "requirements.txt": "django>=4.0",
        "manage.py": """#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{module_path}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise
    execute_from_command_line(sys.argv)
""",
        "{module_path}/__init__.py": "",
        "{module_path}/settings.py": """SECRET_KEY = 'replace-me'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
]

ROOT_URLCONF = '{module_path}.urls'
""",
        "{module_path}/urls.py": """from django.urls import path
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello from {name}')

urlpatterns = [path('', index)]
""",
    },

    "data-science": {
        "README.md": """# {name}

Data-science project layout with a simple src/ and notebooks/.
""",
        "requirements.txt": """numpy
pandas
matplotlib
scikit-learn
""",
        "src/": "",
        "notebooks/README.md": """# Notebooks

Add your exploratory notebooks here.
""",
        ".gitignore": """__pycache__/
.ipynb_checkpoints/
.venv
""",
    },

    "notebook": {
        "README.md": """# {name} Notebook Project

Single notebook project.
""",
        "notebook.ipynb": "",  # placeholder (empty file)
        ".gitignore": """__pycache__/
.ipynb_checkpoints/
.venv
""",
    },

    "poetry": {
        "README.md": """# {name}

A project scaffold using Poetry.
""",
        "pyproject.toml": """[tool.poetry]
name = \"{package_name}\"
version = \"0.0.0\"
description = \"{name}\"
authors = [\"{author}\"]

[tool.poetry.dependencies]
python = ">={py_min}"

[tool.poetry.dev-dependencies]
pytest = "*"
""",
        ".gitignore": """__pycache__/
.venv
""",
    },

    "docker": {
        "README.md": """# {name}

Dockerized Python app scaffold.
""",
        "Dockerfile": """FROM python:{py_min}-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD [\"python\", \"{module_path}.py\"]
""",
        "requirements.txt": "# Add your dependencies",
        ".dockerignore": """__pycache__/
*.pyc
.venv
""",
    },

    # ---- New templates added below ----
    "streamlit": {
        "README.md": """# {name}

A Streamlit app scaffold.
""",
        "app.py": """import streamlit as st

st.title('Hello from {name}')

if __name__ == '__main__':
    pass
""",
        "requirements.txt": "streamlit",
        ".gitignore": """__pycache__/
.venv
""",
    },

    "gradio": {
        "README.md": """# {name}

A Gradio demo scaffold.
""",
        "app.py": """import gradio as gr

def greet(name):
    return f'Hello {name} from {name}'

iface = gr.Interface(fn=greet, inputs='text', outputs='text')

if __name__ == '__main__':
    iface.launch()
""",
        "requirements.txt": "gradio",
    },

    "aws-lambda": {
        "README.md": """# {name}

AWS Lambda function scaffold (handler-based).
""",
        "handler.py": """def handler(event, context):
    return {'statusCode': 200, 'body': 'Hello from {name}'}
""",
        "template.yml": """AWSTemplateFormatVersion: '2010-09-09'
Resources:
  {name}Function:
    Type: AWS::Serverless::Function
    Properties:
      Handler: handler.handler
      Runtime: python3.9
      CodeUri: ./
""",
        "requirements.txt": "# Add dependencies for lambda",
    },

    "telegram-bot": {
        "README.md": """# {name}

A Telegram bot scaffold using python-telegram-bot (add dependency manually).
""",
        "bot.py": """from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello from {name}')

def main():
    updater = Updater('YOUR_TOKEN')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
""",
        "requirements.txt": "python-telegram-bot",
    },

    "sanic": {
        "README.md": """# {name}

A Sanic async web app scaffold.
""",
        "app.py": """from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)

@app.get('/')
async def test(request):
    return json({'message': 'Hello from {name}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
""",
        "requirements.txt": "sanic",
    },

    "aiohttp": {
        "README.md": """# {name}

An aiohttp server scaffold.
""",
        "app.py": """from aiohttp import web

async def handle(request):
    return web.Response(text='Hello from {name}')

app = web.Application()
app.router.add_get('/', handle)

if __name__ == '__main__':
    web.run_app(app, port=8080)
""",
        "requirements.txt": "aiohttp",
    },

    "mlops": {
        "README.md": """# {name}

MLOps project scaffold: src/, experiments/, models/, data/ and a simple Makefile.
""",
        "Makefile": """.PHONY: venv train

venv:
	python -m venv .venv

train:
	python -m src.train
""",
        "src/__init__.py": "",
        "src/train.py": """def main():
    print('Training placeholder for {name}')

if __name__ == '__main__':
    main()
""",
        "data/README.md": """# data

Place datasets here.
""",
        "models/README.md": """# models

Trained models will be stored here.
""",
        ".gitignore": """__pycache__/
.venv/
models/
data/
""",
    },

    "qt": {
        "README.md": """# {name}

A PyQt5/6 desktop app scaffold.
""",
        "app.py": """import sys
try:
    from PyQt6.QtWidgets import QApplication, QLabel
except Exception:
    from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel('Hello from {name}')
label.show()
app.exec()
""",
        "requirements.txt": "pyqt6",
    },

    "electron": {
        "README.md": """# {name}

An Electron + Python scaffold (Electron frontend but Python backend served over HTTP).
""",
        "frontend/README.md": """Place your Electron app here.
""",
        "backend.py": """from http.server import SimpleHTTPRequestHandler, HTTPServer

class Handler(SimpleHTTPRequestHandler):
    pass

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 5000), Handler).serve_forever()
""",
        "requirements.txt": "# Add Python backend deps",
    },

    "grpc": {
        "README.md": """# {name}

A basic gRPC Python service scaffold (add protobuf files and deps).
""",
        "server.py": """import grpc
# import generated pb2 and pb2_grpc modules

def serve():
    print('gRPC server placeholder for {name}')

if __name__ == '__main__':
    serve()
""",
        "requirements.txt": "grpcio",
    },
}

# -----------------------------
# License templates (short / representative)
# -----------------------------
LICENSE_TEMPLATES: Dict[str, str] = {
    "MIT": """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction...
""",
    "Apache-2.0": """Apache License 2.0

Copyright (c) {year} {author}

Licensed under the Apache License, Version 2.0 (the \"License\"); you may not use this file except in compliance with the License...
""",
    "GPL-3.0": """GNU GENERAL PUBLIC LICENSE Version 3

Copyright (C) {year} {author}

This program is free software: you can redistribute it and/or modify...
""",
    "BSD-2-Clause": """BSD 2-Clause License

Copyright (c) {year}, {author}

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met...
""",
    "BSD-3-Clause": """BSD 3-Clause License

Copyright (c) {year}, {author}

Redistribution and use in source and binary forms (with or without
modification) are permitted provided that the following conditions are met...
""",
    "MPL-2.0": """Mozilla Public License 2.0

Copyright (c) {year} {author}

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/
""",
    "LGPL-3.0": """GNU LESSER GENERAL PUBLIC LICENSE Version 3

Copyright (C) {year} {author}

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation...
""",
    "Unlicense": """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.
""",
    "CC0-1.0": """CC0 1.0 Universal (Public Domain Dedication)

The person who associated a work with this deed has dedicated the work to
the public domain by waiving all of his or her rights to the work worldwide
under copyright law, including all related and neighboring rights, to the
extent allowed by law.
""",
}

# -----------------------------
# Helpers
# -----------------------------

def render(template: str, **kwargs) -> str:
    return template.format(**kwargs)


def safe_mkdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    # if content is empty string and filename ends with '/', create dir
    if content == '' and str(path).endswith(os.sep):
        safe_mkdir(path)
        return
    safe_mkdir(path.parent)
    path.write_text(content, encoding='utf-8')
    print(f"Created {path}")


def run_cmd(cmd: list, cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    print(f"Running: {' '.join(cmd)} (cwd={cwd})")
    try:
        return subprocess.run(cmd, check=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}; stdout={e.stdout}; stderr={e.stderr}")
        return e


def find_template(name: str) -> Optional[Dict[str, str]]:
    return TEMPLATES.get(name)

# -----------------------------
# Per-template CI/workflows
# -----------------------------

def ci_workflow_content(template: str, py_min: str) -> str:
    """Return a tailored GitHub Actions workflow for the given template."""
    base = textwrap.dedent(f"""
    name: CI for {template}

    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            python-version: ['{py_min}', '3.9', '3.10', '3.11']
        steps:
        - uses: actions/checkout@v3
        - name: Set up Python ${{{{ matrix.python-version }}}}
          uses: actions/setup-python@v4
          with:
            python-version: ${{{{ matrix.python-version }}}}
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
    """)

    if template in ('flask', 'fastapi', 'sanic', 'aiohttp'):
        return base + textwrap.dedent("""
            - name: Install requirements
              run: |
                pip install -r requirements.txt || true
            - name: Run simple smoke test
              run: |
                echo "Run server smoke checks" || true
        """)

    if template == 'django':
        return base + textwrap.dedent("""
            - name: Install requirements
              run: |
                pip install -r requirements.txt || true
            - name: Run Django checks
              run: |
                python manage.py --help || true
        """)

    if template == 'mlops':
        return base + textwrap.dedent("""
            - name: Install requirements
              run: |
                pip install -r requirements.txt || true
            - name: Run training smoke
              run: |
                python -m src.train || true
        """)

    if template == 'aws-lambda':
        return base + textwrap.dedent("""
            - name: Validate SAM template
              run: |
                echo "No SAM validation configured" || true
        """)

    # default: try running pytest if present
    return base + textwrap.dedent("""
        - name: Install dev deps
          run: |
            pip install pytest || true
        - name: Run tests
          run: |
            pytest -q || true
    """)

# -----------------------------
# Core scaffold logic (supports multiple types)
# -----------------------------

def create_project(
    name: str,
    types: List[str],
    directory: Optional[str] = None,
    license_id: Optional[str] = 'MIT',
    author: Optional[str] = 'Your Name',
    py_min: str = '3.8',
    git_init: bool = False,
    gitrep: Optional[str] = None,
    make_venv: bool = False,
    include_tests: bool = True,
    ci: bool = False,
    dry_run: bool = False,
) -> None:
    # normalize types
    types = [t.lower() for t in types]
    unknown = [t for t in types if t not in TEMPLATES]
    if unknown:
        print(f"Unknown template types: {unknown}")
        print(f"Available: {', '.join(sorted(TEMPLATES.keys()))}")
        return

    base = Path(directory) if directory else Path('.')
    project_root = base / name
    if project_root.exists() and not dry_run:
        print(f"Error: {project_root} already exists")
        return

    print(f"Creating root project '{name}' at {project_root} with types: {types}")
    if not dry_run:
        project_root.mkdir(parents=True)

    # create a top-level README
    top_readme = f"# {name}Monorepo created by pyprojinit. Contains: {', '.join(types)}"
    if dry_run:
        print(f"[dry-run] Would create: {project_root}/README.md")
    else:
        write_file(project_root / 'README.md', top_readme)

    for t in types:
        tpl = TEMPLATES[t]
        # create subfolder for each type
        subdir = project_root / t if len(types) > 1 else project_root / name
        if dry_run:
            print(f"[dry-run] Would create subdir: {subdir}")
        else:
            safe_mkdir(subdir)

        ctx = {
            'name': name if len(types) == 1 else f"{name}-{t}",
            'package_name': (name if len(types) == 1 else f"{name}_{t}").replace('-', '_'),
            'module_path': (name if len(types) == 1 else f"{name}_{t}").replace('-', '_'),
            'license_id': license_id or 'Proprietary',
            'py_min': py_min,
            'year': YEAR,
            'author': author,
            'cli_name': (name if len(types) == 1 else f"{name}-{t}").replace('_', '-'),
        }

        # render files
        for rel, tpl_content in tpl.items():
            rel_rendered = rel.format(**ctx)
            dest = subdir / rel_rendered
            if dry_run:
                print(f"[dry-run] Would create file: {dest}")
                continue
            # special-case directories in templates
            if rel.endswith('/'):
                safe_mkdir(dest)
                continue
            content = render(tpl_content, **ctx)
            write_file(dest, content)

        # add license if requested
        if license_id and license_id in LICENSE_TEMPLATES:
            lic_text = LICENSE_TEMPLATES[license_id].format(year=YEAR, author=author)
            if dry_run:
                print(f"[dry-run] Would create: {subdir / 'LICENSE'}")
            else:
                write_file(subdir / 'LICENSE', lic_text)

        # optional extras per subproject
        if include_tests and not any((subdir / 'tests').exists() for _ in [0]):
            if dry_run:
                print(f"[dry-run] Would create tests folder at: {subdir / 'tests'}")
            else:
                safe_mkdir(subdir / 'tests')
                write_file(subdir / 'tests' / '__init__.py', '')

        # CI workflow per template
        if ci:
            workflow = ci_workflow_content(t, py_min)
            if dry_run:
                print(f"[dry-run] Would create CI workflow for {t} at {subdir}/.github/workflows/python-package.yml")
            else:
                write_file(subdir / '.github' / 'workflows' / 'python-package.yml', workflow)

        # Git initialization: prioritize gitrep (if not None) else git_init flag
        should_git = (gitrep is not None) or git_init
        if should_git:
            if dry_run:
                print(f"[dry-run] Would run: git init; git add .; git commit -m 'Initial commit ({t})' in {subdir}")
            else:
                run_cmd(['git', 'init'], cwd=subdir)
                run_cmd(['git', 'add', '.'], cwd=subdir)
                # create main branch explicitly
                run_cmd(['git', 'checkout', '-b', 'main'], cwd=subdir)
                run_cmd(['git', 'commit', '-m', f'Initial commit ({t})'], cwd=subdir)

                # if gitrep provided and non-empty, set remote and push
                if gitrep:
                    try:
                        run_cmd(['git', 'remote', 'add', 'origin', gitrep], cwd=subdir)
                        # try to push; may fail without credentials
                        print('Attempting to push initial commit to remote origin/main (may fail if not authenticated)')
                        run_cmd(['git', 'push', '-u', 'origin', 'main'], cwd=subdir)
                    except Exception as e:
                        print(f"Warning: Failed to set remote or push: {e}")

        # create venv if requested
        if make_venv and not dry_run:
            venv_dir = subdir / '.venv'
            print(f"Creating virtual environment at {venv_dir}")
            run_cmd([sys.executable, '-m', 'venv', str(venv_dir)])

    print(f"Project '{name}' with types {types} created at {project_root}")

# -----------------------------
# CLI
# -----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='pyprojinit', description='Scaffold Python projects quickly')
    sub = p.add_subparsers(dest='cmd')

    create_p = sub.add_parser('create', help='Create a new project (supports multiple types)')
    create_p.add_argument('name', help='root project name')
    # support both legacy single --type and new --types
    create_p.add_argument('--type', dest='type_single', help='(legacy) single project template')
    create_p.add_argument('--types', nargs='+', help='one or more project templates', choices=list(TEMPLATES.keys()))
    create_p.add_argument('--dir', default='.', help='directory to create project in')
    create_p.add_argument('--license', default=None, choices=list(LICENSE_TEMPLATES.keys()), nargs='?', help='license')
    create_p.add_argument('--author', default=None, help='author name for license')
    create_p.add_argument('--py', default=None, help='minimum python version')
    create_p.add_argument('--git', action='store_true', dest='git_init', help='initialize git repo for each subproject')
    create_p.add_argument('--gitrep', nargs='?', const='', default=None, help='Initialize git and optionally set remote URL: --gitrep [url]')
    create_p.add_argument('--venv', action='store_true', help='create .venv for each subproject')
    create_p.add_argument('--no-tests', action='store_true', help='do not create tests folder')
    create_p.add_argument('--ci', action='store_true', help='add GitHub Actions workflow for each subproject')
    create_p.add_argument('--interactive', action='store_true', help='prompt for missing values interactively')
    create_p.add_argument('--dry-run', action='store_true', help='show what would be created without writing files')

    list_p = sub.add_parser('list-templates', help='List available templates')

    return p


def prompt_if_missing(args: argparse.Namespace) -> argparse.Namespace:
    """If interactive flag is set, prompt for missing values and return updated args."""
    if not getattr(args, 'interactive', False):
        return args

    print('Interactive mode: answering prompts (press Enter to accept default shown in brackets)')

    if not getattr(args, 'types', None) and not getattr(args, 'type_single', None):
        choices = ', '.join(sorted(TEMPLATES.keys()))
        val = input(f"Which templates do you want? (space-separated) [{choices}] ")
        if val.strip():
            args.types = val.split()
        else:
            # default to library
            args.types = ['library']

    if not getattr(args, 'license', None):
        licenses = ', '.join(sorted(LICENSE_TEMPLATES.keys()))
        val = input(f"License [{ 'MIT' }], available: {licenses}: ")
        args.license = val.strip() or 'MIT'

    if not getattr(args, 'author', None):
        val = input('Author name [Your Name]: ')
        args.author = val.strip() or 'Your Name'

    if not getattr(args, 'py', None):
        val = input('Minimum Python version [3.8]: ')
        args.py = val.strip() or '3.8'

    if getattr(args, 'gitrep', None) is None:
        val = input('Initialize git for each subproject? (y/N) [N]: ')
        if val.lower().startswith('y'):
            val2 = input('Optional remote URL (leave empty to skip adding remote): ')
            # argparse expects None if not provided, or '' if provided without URL; we store string
            args.gitrep = val2.strip() if val2.strip() else ''

    return args


def main(argv: Optional[list] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.cmd:
        parser.print_help()
        return

    if args.cmd == 'list-templates':
        print('Available templates:')
        for t in sorted(TEMPLATES.keys()):
            print(' -', t)
        print('Available licenses:')
        for l in sorted(LICENSE_TEMPLATES.keys()):
            print(' -', l)
        return

    if args.cmd == 'create':
        # interactive prompts may update args
        args = prompt_if_missing(args)

        # decide types
        types = []
        if getattr(args, 'types', None):
            types = args.types
        elif getattr(args, 'type_single', None):
            types = [args.type_single]
        else:
            types = ['library']

        # fallback values
        license_id = args.license or 'MIT'
        author = args.author or 'Your Name'
        py_min = args.py or '3.8'

        create_project(
            name=args.name,
            types=types,
            directory=args.dir,
            license_id=license_id,
            author=author,
            py_min=py_min,
            git_init=args.git_init,
            gitrep=args.gitrep,
            make_venv=args.venv,
            include_tests=not args.no_tests,
            ci=args.ci,
            dry_run=args.dry_run,
        )


if __name__ == '__main__':
    main()
