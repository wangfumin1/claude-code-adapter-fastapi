# Security Policy

[中文](/SECURITY.md) | English

## Supported Versions

Currently supported versions for security updates:

| Version | Support Status         |
|---------|-----------------------|
| 1.1.x   | ✅ Security updates supported |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it as follows:

1. **Do Not Report Publicly** - Avoid reporting security issues in GitHub Issues or public forums.

2. **Private Reporting** - Send an email to wangfumin2@163.com.

3. **Report Details Should Include**:
   - Detailed description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fixes (if applicable)

## Security Best Practices

### Configuration Security
- Do not hardcode API keys in configuration files
- Use environment variables for sensitive information
- Rotate API keys regularly

### Network Security
- Use HTTPS in production environments
- Configure appropriate CORS policies
- Restrict access sources

### Dependency Security
- Regularly update dependencies
- Use dependency vulnerability scanning tools
- Review the security of third-party dependencies

## Response Time

We commit to:
- Acknowledging receipt of vulnerability reports within 48 hours
- Providing a preliminary assessment within 7 days
- Prioritizing fixes based on vulnerability severity

## Acknowledgments

Thank you to all researchers and users who responsibly report security issues.
