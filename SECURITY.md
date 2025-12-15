# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Helix seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

### How to Report

1. **Email**: Send a detailed report to the repository maintainer via GitHub's private vulnerability reporting feature or contact the owner directly.

2. **Include the following information**:
   - Type of vulnerability (e.g., injection, authentication bypass, data exposure)
   - Full paths of source file(s) related to the vulnerability
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue and how an attacker might exploit it

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours. 
- **Communication**: We will keep you informed of the progress towards a fix and full announcement.
- **Resolution**: We aim to resolve critical vulnerabilities within 7 days and other issues within 30 days. 
- **Credit**: We will credit you in the release notes (unless you prefer to remain anonymous).

## Security Best Practices for Helix Users

### Environment Variables

- **Never commit `.env` files** to version control
- Use `.env.example` as a template and create your own `.env` locally
- Rotate API keys regularly (DeepSeek, Groq, OpenRouter)
- Use strong, unique API keys for each environment

### Redis Security

- Do not expose Redis ports publicly in production
- Use Redis authentication (`requirepass`) in production environments
- Consider using Redis TLS for encrypted connections

### Network Security

- Run Helix behind a reverse proxy (nginx, Traefik) in production
- Enable HTTPS/TLS termination at the proxy level
- Restrict access to internal networks when possible
- Use firewall rules to limit incoming connections

### Docker Security

- Keep Docker and Docker Compose updated
- Do not run containers as root in production
- Use Docker secrets for sensitive data
- Regularly update base images for security patches

### API Keys

```bash
# Good:  Use environment variables
HELIX_OPENROUTER_API_KEY=sk-or-v1-xxxx
HELIX_GROQ_API_KEY=gsk_xxxx

# Bad: Never hardcode keys in source code
api_key = "sk-or-v1-xxxx"  # DON'T DO THIS
```

### Session Management

- Use unique `X-Session-ID` headers for different testing contexts
- Clear sessions after testing sensitive scenarios
- Do not use predictable session IDs in production tests

## Known Security Considerations

### Intended Use Case

Helix is designed as a **development and testing tool**. It should NOT be used as: 
- A production API server
- A public-facing service without authentication
- A replacement for real backend security measures

### Data Sensitivity

- Helix generates mock data and caches responses in Redis
- Do not send real sensitive data (PII, credentials) to Helix
- Clear Redis cache before sharing environments

### AI Provider Communication

- API calls to AI providers (DeepSeek, Groq, Ollama) transmit request context
- Do not include sensitive data in mock requests when using external AI providers
- Consider using `demo` mode or local Ollama for sensitive development work

## Security Updates

Security updates will be released as patch versions and announced in:
- GitHub Releases
- CHANGELOG.md

## Contact

For security-related inquiries, please use GitHub's private vulnerability reporting feature on this repository. 

---

Thank you for helping keep Helix and its users safe!