\# Security Policy



This repository contains educational projects and demo applications.  

No personal data is intentionally stored in this repository.



\## Supported Content

\- Source code for demo projects

\- Documentation and configuration files

\- Example notebooks (without sensitive data)



\## Reporting a Vulnerability

If you find a security issue (for example: exposed secrets, unsafe deserialization, insecure file handling, or dependency vulnerabilities), please open a GitHub Issue with:



\- A clear title (e.g., “Potential secret exposed in <file>”)

\- Steps to reproduce (if applicable)

\- Affected file(s) and line numbers

\- Expected vs actual behavior

\- Suggested mitigation (optional)



\## Safety Notes

\- Do \*\*not\*\* commit secrets (API keys, tokens, passwords).

\- Trained model artifacts (e.g., `.pkl`, `.joblib`) are intentionally excluded.

\- Generated datasets (CSV exports) are intentionally excluded.

\- Avoid loading serialized artifacts (pickle/joblib) from untrusted sources.



\## Dependency \& Vulnerability Checks

This repository includes basic automated checks via GitHub Actions and dependency scanning configuration (where supported by GitHub).

