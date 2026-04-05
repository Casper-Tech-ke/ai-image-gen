# Contributing to AI Imager

Thank you for your interest in contributing to AI Imager! This guide covers everything you need to get started.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Submitting Changes](#submitting-changes)
- [Style Guide](#style-guide)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

---

## Code of Conduct

By participating in this project, you agree to maintain a respectful and constructive environment. Harassment, discrimination, and abusive behaviour will not be tolerated.

---

## How to Contribute

There are many ways to contribute:

- 🐛 **Bug reports** — Open an issue with clear reproduction steps
- 💡 **Feature requests** — Open an issue describing the feature and its use case
- 🔧 **Code contributions** — Fork, branch, commit, and open a pull request
- 📝 **Documentation** — Improve the README, docstrings, or add new guides
- 🔒 **Security** — See [SECURITY.md](SECURITY.md) for responsible disclosure

---

## Development Setup

### Prerequisites

- Python 3.8+
- pip

### Steps

```bash
# 1. Fork the repository on GitHub, then clone your fork
git clone https://github.com/<your-username>/ai-imager.git
cd ai-imager

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the development server
python run.py
```

The server starts on `http://localhost:5000`.

---

## Project Structure

```
ai-imager/
├── ai_imager/               # Core Flask application package
│   ├── __init__.py          # Package init, error handlers
│   ├── imager.py            # AI API integration (Casper Tech APIs)
│   ├── web_interface.py     # Flask routes and request handlers
│   └── common.py            # Shared utilities (history, session, etc.)
├── contents/
│   ├── static/
│   │   ├── css/style.css    # All styles (dark theme)
│   │   ├── javascript/      # Frontend JS
│   │   └── image/           # Static images and favicon
│   └── templates/
│       ├── base.html        # Base layout (nav, footer)
│       ├── index.html       # Landing page
│       ├── form.html        # Image generation form
│       ├── docs.html        # API reference page
│       ├── json_pretty.html # Branded JSON response viewer
│       └── legal/           # Terms, Privacy, Disclaimer pages
├── run.py                   # App entry point (Replit / direct)
├── requirements.txt
├── README.md
├── LICENSE
├── SECURITY.md
└── CONTRIBUTING.md
```

---

## Submitting Changes

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes.** Keep commits focused and atomic.

3. **Test your changes** by running `python run.py` and verifying functionality in your browser.

4. **Commit with a clear message**:
   ```bash
   git commit -m "feat: add support for XYZ"
   ```
   Follow [Conventional Commits](https://www.conventionalcommits.org/) where possible:
   - `feat:` — new feature
   - `fix:` — bug fix
   - `docs:` — documentation only
   - `style:` — formatting, no logic change
   - `refactor:` — code restructure without feature change
   - `chore:` — tooling, dependencies

5. **Push and open a pull request**:
   ```bash
   git push origin feat/your-feature-name
   ```
   Then open a PR on GitHub. Fill in the PR template and link any related issues.

---

## Style Guide

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/). Use `black` for formatting if possible.
- **HTML/CSS**: Maintain the existing dark theme variable system (`var(--text)`, `var(--card)`, etc.).
- **JavaScript**: Plain ES6+, no build step required.
- **No new dependencies** without discussion — keep the footprint minimal.

---

## Reporting Bugs

Open an issue and include:

- Your Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected vs. actual behaviour
- Any relevant error messages or screenshots

---

## Feature Requests

Open an issue titled `[Feature] Your Feature Name` and describe:

- The problem you're trying to solve
- Your proposed solution
- Any alternatives you considered

---

## Questions?

Feel free to open a discussion or reach out via [xcasper.space](https://xcasper.space).
