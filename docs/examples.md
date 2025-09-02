# Example Project Structure 📂

**Multi-template project `mycombo` with `flask` and `mlops`:**

```

mycombo/  
├─ README.md  
├─ flask/  
│ ├─ app.py  
│ ├─ requirements.txt  
│ ├─ LICENSE  
│ └─ tests/  
├─ mlops/  
│ ├─ src/  
│ ├─ requirements.txt  
│ ├─ LICENSE  
│ └─ tests/  
└─ .gitignore

```

<details>
<summary>Tip: Monorepo naming convention</summary>

- Subproject folders are named after the template: `myproject/flask`, `myproject/mlops`
- Python package names replace `-` with `_`, e.g., `myproject_flask`

</details>
