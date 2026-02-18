# Contributing

Thanks for your interest in contributing! This list is community-driven and welcomes additions.

## Adding a New Entry

1. Fork the repository
2. Edit the appropriate JSON file in `data/`
3. Run `python3 scripts/generate_readme.py` to update README
4. Submit a pull request

## Data Files

| File | Contents |
|------|----------|
| `vendors.json` | Security vendors (public, private, MSP) |
| `opensource.json` | Open source security tools |
| `threat-research.json` | Security research teams/labs |
| `acquisitions.json` | M&A activity |
| `cloud-platforms.json` | AWS/GCP/Azure native services |
| `frameworks.json` | Compliance frameworks & glossary |
| `community.json` | Newsletters, podcasts, conferences |

## Entry Format

### Vendors (private)
```json
{"name": "Company", "url": "https://...", "linkedin": "https://linkedin.com/company/...", "crunchbase": "https://crunchbase.com/organization/..."}
```

### Open Source
```json
{"name": "Project", "url": "https://github.com/..."}
```

### Acquisitions
```json
{"target": "Company", "acquirer": "Buyer", "amount": "$100M", "date": "2024-01", "url": "https://..."}
```

## Guidelines

- Verify all URLs are working before submitting
- Keep entries alphabetically sorted within their category
- Include LinkedIn/Crunchbase links for vendors when available
- For acquisitions, include announcement URL if public

## Validation

Run link checker before submitting:
```bash
python3 scripts/validate_links.py
```
