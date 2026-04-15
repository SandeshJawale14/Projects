\# Contributing Guidelines



Thanks for taking the time to contribute.



\## General Guidelines

\- Keep changes small and focused.

\- Use clear commit messages (e.g., “Fix forecast date frequency for pandas 3.x”).

\- Prefer readable code over clever code.



\## Security \& Safety

\- Do not commit secrets (tokens, keys, passwords).

\- Do not commit large or generated artifacts:

&#x20; - `venv/`

&#x20; - `models/\*.pkl`, `models/\*.joblib`

&#x20; - `data/\*.csv`

&#x20; - logs or reports

\- Avoid using `pickle/joblib` to load files from untrusted sources.



\## Running Checks Locally (Optional)

If you want to run basic security checks:

\- `pip-audit` for dependency vulnerabilities

\- `bandit` for simple Python security linting



Example:

```bash

pip install pip-audit bandit

pip-audit

bandit -r .

