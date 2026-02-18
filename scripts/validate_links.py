#!/usr/bin/env python3
"""Validate all URLs in JSON data files."""
import json
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed

DATA_DIR = Path(__file__).parent.parent / "data"

def extract_urls(obj, urls=None):
    if urls is None:
        urls = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("url", "linkedin", "crunchbase", "shared_responsibility", "overview") and isinstance(v, str):
                urls.append(v)
            else:
                extract_urls(v, urls)
    elif isinstance(obj, list):
        for item in obj:
            extract_urls(item, urls)
    return urls

def check_url(url, timeout=10):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (link checker)"})
        with urlopen(req, timeout=timeout) as resp:
            return url, resp.status, None
    except HTTPError as e:
        return url, e.code, str(e)
    except URLError as e:
        return url, None, str(e.reason)
    except Exception as e:
        return url, None, str(e)

def main():
    urls = set()
    for f in DATA_DIR.glob("*.json"):
        data = json.loads(f.read_text())
        urls.update(extract_urls(data))

    print(f"Checking {len(urls)} URLs...")
    failed = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_url, url): url for url in urls}
        for future in as_completed(futures):
            url, status, error = future.result()
            if status and 200 <= status < 400:
                print(f"✓ {url}")
            else:
                print(f"✗ {url} - {error or status}")
                failed.append((url, error or status))

    if failed:
        print(f"\n{len(failed)} URLs failed:")
        for url, err in failed:
            print(f"  {url}: {err}")
        sys.exit(1)
    print("\nAll URLs valid!")

if __name__ == "__main__":
    main()
