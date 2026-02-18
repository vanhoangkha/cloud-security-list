#!/usr/bin/env python3
"""Generate README.md from JSON data files."""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUT = Path(__file__).parent.parent / "README.md"

HEADER = """# Cloud Security List

[![Validate Links](https://github.com/someengineering/cloud-security-list/actions/workflows/validate.yml/badge.svg)](https://github.com/someengineering/cloud-security-list/actions/workflows/validate.yml)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

> A curated list of cloud security tools, vendors, and resources.

Cloud security engineers are notoriously overworked and under-resourced. This list has links to tools, frameworks and resources to make their lives easier.

## 🌐 [Browse the interactive site →](https://someengineering.github.io/cloud-security-list/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new entries.

---
"""

def load(name):
    return json.loads((DATA_DIR / f"{name}.json").read_text())

def link(name, url):
    return f"[{name}]({url})"

def main():
    lines = [HEADER]

    # Threat Research
    lines.append("# Threat Research\n")
    for r in load("threat-research"):
        lines.append(f"- {link(r['name'], r['url'])}")
    lines.append("")

    # Vendors
    vendors = load("vendors")
    lines.append("# Security Vendors\n")
    lines.append("## Publicly Listed Vendors\n")
    lines.append("These are vendors with publicly traded stocks. Links: website, LinkedIn, stock ticker.\n")
    for v in vendors["public"]:
        ticker_url = f"https://finance.yahoo.com/quote/{v['ticker']}"
        lines.append(f"- {link(v['name'], v['url'])} | {link('LinkedIn', v['linkedin'])} | {link(v['ticker'], ticker_url)}")
    lines.append("\n### Formerly Listed\n")
    for v in vendors["formerly_public"]:
        ticker_url = f"https://finance.yahoo.com/quote/{v['ticker']}"
        lines.append(f"- {link(v['name'], v['url'])} | {link('LinkedIn', v['linkedin'])} | {link(v['ticker'], ticker_url)}")
    lines.append("\n## Private Vendors\n")
    lines.append("Venture-funded companies\n")
    for v in vendors["private"]:
        lines.append(f"- {link(v['name'], v['url'])} | {link('LinkedIn', v['linkedin'])} | {link('Crunchbase', v['crunchbase'])}")
    lines.append("\n## Managed Service Providers\n")
    for v in vendors["msp"]:
        lines.append(f"- {link(v['name'], v['url'])} | {link('LinkedIn', v['linkedin'])} | {link('Crunchbase', v['crunchbase'])}")
    lines.append("")

    # Acquisitions
    lines.append("# Acquisitions\n")
    for a in sorted(load("acquisitions"), key=lambda x: x["date"], reverse=True):
        amt = f", {a['amount']}" if a["amount"] else ""
        url_part = f" - {link('announcement', a['url'])}" if a["url"] else ""
        lines.append(f"- **{a['target']}** → {a['acquirer']} ({a['date']}{amt}){url_part}")
    lines.append("")

    # Cloud Platforms
    platforms = load("cloud-platforms")
    lines.append("# Cloud Platforms\n")
    for cloud, data in platforms.items():
        lines.append(f"## {cloud.upper()}\n")
        if "shared_responsibility" in data:
            lines.append(f"- {link('Shared Responsibility Model', data['shared_responsibility'])}")
        if "overview" in data:
            lines.append(f"- {link('Security Overview', data['overview'])}")
        for svc in data.get("services", []):
            lines.append(f"- {link(svc['name'], svc['url'])}")
        lines.append("")

    # Open Source (grouped by category)
    opensource = load("opensource")
    lines.append("# Open Source Projects\n")
    categories = {}
    for p in opensource:
        cat = p.get("category", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
    
    cat_names = {
        "cspm": "Cloud Security Posture Management",
        "iac": "Infrastructure as Code Security", 
        "kubernetes": "Kubernetes Security",
        "container": "Container Security",
        "aws": "AWS Security",
        "azure": "Azure Security",
        "gcp": "GCP Security",
        "iam": "IAM Security",
        "inventory": "Asset Inventory",
        "runtime": "Runtime Security",
        "pentest": "Penetration Testing",
        "governance": "Governance",
        "vulnerability": "Vulnerability Management",
        "siem": "SIEM",
        "forensics": "Forensics",
        "recon": "Reconnaissance",
        "training": "Training",
        "supply-chain": "Supply Chain Security"
    }
    for cat in sorted(categories.keys()):
        lines.append(f"### {cat_names.get(cat, cat.title())}\n")
        for p in sorted(categories[cat], key=lambda x: x["name"].lower()):
            lines.append(f"- {link(p['name'], p['url'])}")
        lines.append("")

    # Frameworks & Glossary
    fw = load("frameworks")
    lines.append("# Security Categories / Glossary\n")
    for abbr, full in sorted(fw["glossary"].items()):
        lines.append(f"- **{abbr}** - {full}")
    lines.append("\n# Security Frameworks\n")
    for f in fw["frameworks"]:
        lines.append(f"- {link(f['name'], f['url'])}")
    lines.append("\n# Security Resources\n")
    for r in fw["resources"]:
        lines.append(f"- {link(r['name'], r['url'])}")
    lines.append("")

    # Community
    comm = load("community")
    lines.append("# Security Newsletters\n")
    for n in comm["newsletters"]:
        lines.append(f"- {link(n['name'], n['url'])} by {link(n['author'], n['linkedin'])}")
    lines.append("\n# Security Podcasts\n")
    for p in comm["podcasts"]:
        lines.append(f"- {link(p['name'], p['url'])}")
    lines.append("\n# Conferences\n")
    lines.append("## Community\n")
    for c in comm["conferences"]["community"]:
        lines.append(f"- {link(c['name'], c['url'])}")
    lines.append("\n## Industry\n")
    for c in comm["conferences"]["industry"]:
        lines.append(f"- {link(c['name'], c['url'])}")
    lines.append("")

    # Cyber Insurance
    lines.append("# Cyber Insurance\n")
    for i in load("cyber-insurance"):
        lines.append(f"- {link(i['name'], i['url'])} | {link('LinkedIn', i['linkedin'])}")
    lines.append("")

    # Training Labs
    lines.append("# Training & Practice Labs\n")
    for t in load("training-labs"):
        lines.append(f"- {link(t['name'], t['url'])} - {t['description']} ({t['platform']})")

    OUT.write_text("\n".join(lines) + "\n")
    print(f"Generated {OUT}")

if __name__ == "__main__":
    main()
