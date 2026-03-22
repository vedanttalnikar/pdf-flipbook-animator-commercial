# Commercial Deployment Guide

## Repository Setup (Private)

### Step 1: Create Private GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Set repository name: `pdf-flipbook-animator-commercial`
3. **Important**: Set visibility to **Private**
4. Do NOT initialize with README (we already have one)
5. Click "Create repository"

### Step 2: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial.git

# Push code
git branch -M main
git push -u origin main
```

### Step 3: Repository Settings

#### Collaborators & Access
- Go to Settings → Collaborators
- Add team members who need access
- Assign appropriate roles (Admin, Write, Read)

#### Branch Protection
- Go to Settings → Branches
- Add rule for `main` branch:
  - ✅ Require pull request reviews before merging
  - ✅ Require status checks to pass
  - ✅ Require branches to be up to date

#### Secrets (for CI/CD)
- Go to Settings → Secrets and variables → Actions
- Add these secrets:
  - `PYPI_COMMERCIAL_TOKEN` - For private PyPI server
  - `LICENSE_SERVER_KEY` - For license validation
  - `CODECOV_TOKEN` - Optional, for coverage reports

## License Management System

### Recommended: Gumroad Integration
For selling licenses, integrate with Gumroad:

1. **Create Gumroad Account**: https://gumroad.com
2. **Set up Products**:
   - Personal License: $49/year
   - Team License: $199/year  
   - Enterprise License: $599/year
3. **License Key Generation**: Use Gumroad's license key API
4. **Webhook Integration**: Automate license delivery

### Alternative: Custom License Server
Build your own with:
- FastAPI backend
- PostgreSQL for license storage
- Stripe for payments
- JWT tokens for validation

## Distribution Strategy

### Option 1: Private PyPI Server (Recommended)
```bash
# Set up gemfury/cloudsmith
# Install from private repo
pip install --index-url https://pypi.YOUR-DOMAIN.com/simple/ pdf-flipbook-animator
```

### Option 2: Direct Download with License Check
- Host downloadable wheels on your website
- Require license key for download access
- Implement activation endpoint

### Option 3: GitHub Releases (Private)
- Use private repository releases
- Grant access via teams/collaborators
- Provide download links to customers

## Activation System Implementation

### Add License Validation Module

Create `src/pdf_flipbook_animator/license.py`:

```python
import os
import hashlib
import requests
from pathlib import Path

LICENSE_SERVER = "https://api.pdf-flipbook-animator.com/v1/validate"
LICENSE_FILE = Path.home() / ".pdf_flipbook" / "license.key"

def validate_license(license_key: str) -> bool:
    """Validate license key with server."""
    try:
        response = requests.post(
            LICENSE_SERVER,
            json={"license_key": license_key, "version": "0.2.0"},
            timeout=10
        )
        return response.status_code == 200 and response.json().get("valid")
    except:
        # Check cached license
        return check_cached_license(license_key)

def activate_license(license_key: str) -> bool:
    """Activate and save license."""
    if validate_license(license_key):
        LICENSE_FILE.parent.mkdir(exist_ok=True)
        LICENSE_FILE.write_text(license_key)
        return True
    return False

def check_license() -> bool:
    """Check if valid license exists."""
    if LICENSE_FILE.exists():
        return validate_license(LICENSE_FILE.read_text().strip())
    return False
```

### Add Activation Command

Update `cli.py`:
```python
@cli.command()
@click.argument("license_key")
def activate(license_key: str):
    """Activate your license."""
    from pdf_flipbook_animator.license import activate_license
    
    if activate_license(license_key):
        click.echo("✅ License activated successfully!")
    else:
        click.echo("❌ Invalid license key. Please check and try again.")
        click.echo("Need help? Contact vedanttalnikar@gmail.com")
```

## Marketing & Sales

### Website Content
- Landing page: https://pdf-flipbook-animator.com
- Demo page with live examples
- Pricing page with comparison table
- Documentation at docs.pdf-flipbook-animator.com
- Blog for SEO and tutorials

### Marketing Channels
1. **Direct Sales**: Through your website
2. **Marketplaces**: 
   - Gumroad (easiest)
   - Paddle (advanced)
   - FastSpring (enterprise)
3. **Affiliate Program**: 20-30% commission
4. **Volume Licensing**: Contact sales

## Support Infrastructure

### Customer Support
- Email: vedanttalnikar@gmail.com
- Documentation: docs.pdf-flipbook-animator.com
- FAQ page
- Issue tracking via private repo

### Analytics
- Google Analytics for website
- Mixpanel/Amplitude for product usage
- License usage tracking
- Conversion funnel monitoring

## Pricing Strategy

### Tiered Pricing (Annual)
| Plan | Price | Target |
|------|-------|--------|
| Personal | $49 | Individual users, freelancers |
| Team | $199 | Small teams (5 users) |
| Enterprise | $599 | Large organizations |
| Custom | Quote | White-label, API access |

### Add-ons
- Priority support: +$99/year
- White-labeling: +$299/year
- API access: +$199/year
- Custom development: Hourly rate

## Legal Requirements

### Terms of Service
Update website with:
- End User License Agreement (EULA)
- Privacy Policy
- Terms of Service
- Refund Policy (30-day money-back)

### Tax Compliance
- Set up Merchant of Record (Paddle/Gumroad handles this)
- Or use Stripe Tax for automatic tax calculation
- Register business entity (LLC recommended)

## Monitoring & Maintenance

### Key Metrics to Track
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- Churn rate
- Active licenses
- Support ticket volume

### Regular Tasks
- Weekly: Check support tickets
- Monthly: Update dependencies, security patches
- Quarterly: Major feature releases
- Annual: License renewals, customer surveys

## Next Steps

1. ✅ Code is ready (v0.2.0 with animations)
2. ✅ Tests passing (82% coverage)
3. ✅ Git repository initialized
4. ⏳ Create private GitHub repository
5. ⏳ Set up payment processor (Gumroad recommended)
6. ⏳ Build landing page
7. ⏳ Implement license validation
8. ⏳ Launch beta with select customers

## Estimated Timeline

- **Week 1-2**: License system + website
- **Week 3**: Beta testing
- **Week 4**: Public launch
- **Month 2-3**: Marketing push
- **Month 4+**: Feature iterations based on feedback

## Projected Revenue (Conservative)

| Month | Users | MRR | Notes |
|-------|-------|-----|-------|
| 1 | 10 | $400 | Friends & family |
| 3 | 50 | $2,000 | Early adopters |
| 6 | 150 | $6,000 | Organic growth |
| 12 | 400 | $16,000 | Established product |

**First Year Revenue**: ~$50,000 - $100,000 (depending on marketing)

---

**Contact for Implementation Support**:
- Repository: https://github.com/vedanttalnikar/pdf-flipbook-animator-commercial
- Email: vedanttalnikar@gmail.com
