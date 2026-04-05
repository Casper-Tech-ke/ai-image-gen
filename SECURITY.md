# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | ✅ Yes    |
| Older   | ❌ No     |

Only the latest version of AI Imager receives security updates. Please ensure you are running the most recent version before reporting a vulnerability.

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

If you discover a security vulnerability in AI Imager, please report it responsibly:

1. **Email or direct message** the maintainer through the contact details on [xcasper.space](https://xcasper.space).
2. Include the following in your report:
   - A clear description of the vulnerability
   - Steps to reproduce the issue
   - The potential impact (e.g., data exposure, remote code execution)
   - Any suggested mitigations or patches

We aim to respond to security reports within **48 hours** and to release a fix within **7 days** of confirmation.

## Scope

The following are **in scope** for security reports:

- SQL injection, XSS, or other web vulnerabilities in the Flask application
- Path traversal or arbitrary file read/write via upload functionality
- Session fixation or cookie security issues
- Server-side request forgery (SSRF) via prompt or URL inputs
- Sensitive data exposure

The following are **out of scope**:

- Vulnerabilities in third-party APIs (Casper Tech / apis.xcasper.space) — report those to their maintainers
- Denial-of-service via rate limiting (no rate limiting is implemented by design)
- Issues in the underlying OS or hosting infrastructure

## Acknowledgements

We appreciate responsible disclosure and will publicly acknowledge security reporters (with their permission) in the release notes.
