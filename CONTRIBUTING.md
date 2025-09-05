
# Contributing to jyinit

Thanks for your interest in contributing 🎉  
We welcome contributions of all kinds — bug reports, fixes, features, docs, or tests.

---

## 🐛 Reporting Issues

- Use the [GitHub Issues](../../issues) page.
- Clearly describe:
  - What you expected to happen
  - What actually happened
  - Steps to reproduce
- Include your Python version, OS, and `jyinit --version`.

---

## 🌱 Submitting Changes

1. **Fork** the repo and create your branch:
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Install dependencies** for development:
    
    ```bash
    pip install -r requirements-dev.txt
    ```
    
3. **Run tests** locally:
    
    ```bash
    pytest
    ```
    
4. **Commit changes** with a clear message:
    
    ```bash
    git commit -m "feat: add new template xyz"
    ```
    
    Use [Conventional Commits](https://www.conventionalcommits.org/) style:
    
    - `feat:` – new feature
        
    - `fix:` – bug fix
        
    - `docs:` – documentation only
        
    - `test:` – add or fix tests
        
    - `refactor:` – code change without new features/bug fixes
        
5. **Push** your branch and open a **Pull Request**:
    
    ```bash
    git push origin feature/your-feature
    ```
    

---

## ✅ Code Guidelines

- Follow **PEP8** for Python style.
    
- Keep functions small and focused.
    
- Add or update tests for new code.
    
- Update documentation (`README.md` or `docs/`) if needed.
    

---

## 🔬 Testing

Run all tests before submitting:

```bash
pytest
```

If you add a new template, include at least:

- `tests/test_basic.py` import check
    
- Smoke test if applicable
    

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](https://github.com/nj2216/jyinit/blob/main/LICENSE).

---

🙌 Thanks again for helping make **jyinit** better!

---