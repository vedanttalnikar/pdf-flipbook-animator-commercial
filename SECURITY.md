# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of PDF Flipbook Animator seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:

- Open a public GitHub issue for security vulnerabilities
- Publicly disclose the vulnerability before it has been addressed

### Please DO:

1. **Email us**: Send details to the project maintainers via GitHub
2. **Provide details**: Include as much information as possible:
   - Type of vulnerability
   - Full paths of source file(s) related to the vulnerability
   - Location of the affected source code (tag/branch/commit)
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if available)
   - Impact of the vulnerability

### What to expect:

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Timeline**: We aim to resolve critical vulnerabilities within 30 days

### Disclosure Policy

- Security issues will be disclosed publicly only after a fix is available
- We will credit researchers who report vulnerabilities (unless they prefer to remain anonymous)
- We will publish a security advisory on GitHub

## Security Best Practices

When using PDF Flipbook Animator:

### Input Validation

- Only process PDF files from trusted sources
- Validate PDF files before processing
- Be cautious with PDFs from unknown sources (malicious PDFs can exploit vulnerabilities)

### Output Security

- Sanitize any user-provided input used in flipbook titles or metadata
- Host generated flipbooks on secure HTTPS servers
- Implement appropriate Content Security Policy (CSP) headers

### Dependencies

- Keep pip packages up to date
- Monitor for security advisories in dependencies:
  - PyMuPDF
  - Pillow
  - Click

### Hosting

When hosting generated flipbooks:

- Use HTTPS
- Implement appropriate CORS policies
- Set secure HTTP headers
- Consider adding authentication for sensitive content

## Known Security Considerations

### PDF Processing

- PDF files can contain malicious content
- Large or complex PDFs may cause resource exhaustion
- Embedded JavaScript in PDFs is not executed during conversion

### Generated Output

- Generated HTML/CSS/JS contains no server-side code
- JavaScript is minimal and doesn't collect user data
- No external resources loaded except documented CDN libraries
- **External Links (`--preserve-links`)**: When using the `--preserve-links` flag, clickable links from the original PDF are preserved. External URLs (LINK_URI) will open in a new tab. Review the source PDF to ensure linked URLs are trusted before enabling this feature.

### Privacy

- No telemetry or analytics in the tool itself
- Generated flipbooks are static HTML (no tracking unless you add it)
- PDF metadata is not exposed in the generated output by default

## Security Updates

Security updates will be released as patch versions (e.g., 0.1.1) and:

- Will be clearly marked in CHANGELOG.md
- Will be announced in GitHub Releases
- Will include CVE identifiers if applicable

## Dependencies Security

We use:

- **Dependabot**: Automated dependency updates
- **GitHub Security Advisories**: Monitoring for known vulnerabilities
- **Automated CI**: Testing for security issues

## Contact

For security concerns, please contact:
- Email: vedanttalnikar@gmail.com
- GitHub Issues (for non-security bugs)
- [Create a private security advisory on GitHub](https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial/security/advisories/new)

Thank you for helping keep PDF Flipbook Animator secure!
