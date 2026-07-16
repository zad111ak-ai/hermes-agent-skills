# Security Policy

## Reporting a Vulnerability

**NEVER create a public issue for security vulnerabilities!**

📧 Email: [REDACTED]
🔒 GPG Key: Available on request

We will respond within 48 hours.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x.x   | ✅ Active |
| 0.x.x   | ❌ Deprecated |

## Security Best Practices

- Never store secrets in skill files
- Use environment variables for sensitive data
- Validate user inputs before processing
- Use least privilege principle

## Skills Security

Skills may execute commands or access external resources. Always:
- Review skill code before use
- Run skills in isolated environments
- Monitor skill execution logs
- Restrict skill permissions as needed
