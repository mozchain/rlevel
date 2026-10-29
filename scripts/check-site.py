#!/usr/bin/env python3
"""
Rlevel Site Health & SDLC Quality Checker
Verifies link integrity, asset resolution, SEO metadata, sitemap sync, and accessibility.
"""

import os
import sys
import glob
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

errors = []
warnings = []

class HTMLAssetParser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.links = []
        self.images = []
        self.has_title = False
        self.has_desc = False
        self.has_viewport = False
        self.has_canonical = False
        self.in_title = False
        self.title_content = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        if tag == "title":
            self.has_title = True
            self.in_title = True
            
        elif tag == "meta":
            name = attr_dict.get("name", "").lower()
            prop = attr_dict.get("property", "").lower()
            content = attr_dict.get("content", "")
            if name == "description" and content.strip():
                self.has_desc = True
            elif name == "viewport" and content.strip():
                self.has_viewport = True
                
        elif tag == "link":
            rel = attr_dict.get("rel", "").lower()
            href = attr_dict.get("href", "")
            if rel == "canonical" and href.strip():
                self.has_canonical = True
            if href:
                self.links.append((href, self.getpos()))
                
        elif tag == "img":
            src = attr_dict.get("src", "")
            alt = attr_dict.get("alt")
            self.images.append((src, alt, self.getpos()))
            if src:
                self.links.append((src, self.getpos()))
                
        elif tag in ["a", "script", "source"]:
            ref = attr_dict.get("href") or attr_dict.get("src")
            if ref:
                self.links.append((ref, self.getpos()))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_content += data.strip()


def check_html_files():
    print(f"{BLUE}{BOLD}1. Checking HTML Pages & Local Asset References...{RESET}")
    html_files = sorted(glob.glob("*.html"))
    if not html_files:
        errors.append("No .html files found in current directory.")
        return html_files, set()

    all_referenced_assets = set()

    for hf in html_files:
        with open(hf, "r", encoding="utf-8") as f:
            content = f.read()

        parser = HTMLAssetParser(hf)
        parser.feed(content)

        # SEO & Meta checks
        if not parser.has_title or not parser.title_content:
            errors.append(f"{hf}: Missing or empty <title> tag.")
        if not parser.has_desc:
            errors.append(f"{hf}: Missing or empty <meta name=\"description\"> tag.")
        if not parser.has_viewport:
            warnings.append(f"{hf}: Missing <meta name=\"viewport\"> tag.")
        if not parser.has_canonical:
            warnings.append(f"{hf}: Missing <link rel=\"canonical\"> tag (recommended for SEO).")

        # Image alt checks
        for src, alt, (line, col) in parser.images:
            if alt is None:
                errors.append(f"{hf}:{line} <img> tag missing alt attribute: src='{src}'")
            elif alt.strip() == "":
                warnings.append(f"{hf}:{line} <img> tag has empty alt attribute: src='{src}'")

        # Local link resolution
        for ref, (line, col) in parser.links:
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
                continue

            clean_ref = ref.split("?")[0].split("#")[0]
            if not clean_ref:
                continue

            all_referenced_assets.add(clean_ref)

            # Check if file exists relative to root
            target_path = clean_ref.lstrip("/")
            # Support clean urls like /about resolving to about.html
            target_html = f"{target_path}.html"
            
            exists = os.path.exists(target_path) or (not target_path.endswith(".html") and os.path.exists(target_html))
            if not exists:
                errors.append(f"{hf}:{line} Broken reference: '{ref}' not found on disk.")

    print(f"   Checked {len(html_files)} HTML pages.")
    return html_files, all_referenced_assets


def check_sitemap(html_files):
    print(f"{BLUE}{BOLD}2. Checking sitemap.xml Synchronization...{RESET}")
    if not os.path.exists("sitemap.xml"):
        errors.append("sitemap.xml not found in project root.")
        return

    try:
        tree = ET.parse("sitemap.xml")
        root = tree.getroot()
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [loc.text.strip() for loc in root.findall(".//sm:loc", namespace)]
    except Exception as e:
        errors.append(f"Failed to parse sitemap.xml: {e}")
        return

    # Map URLs to expected pages
    base_domain = "https://rlevelcarpentrysolutions.com.au"
    sitemap_paths = []
    for u in urls:
        if not u.startswith(base_domain):
            warnings.append(f"sitemap.xml entry does not start with expected domain {base_domain}: {u}")
        path = u.replace(base_domain, "").strip("/")
        sitemap_paths.append(path)

    # Verify each HTML file has a route in sitemap
    for hf in html_files:
        route = "" if hf == "index.html" else hf.replace(".html", "")
        if route not in sitemap_paths:
            errors.append(f"sitemap.xml missing route for '{hf}' (expected URL: {base_domain}/{route})")

    # Verify each sitemap route corresponds to an existing HTML file
    for sp in sitemap_paths:
        expected_file = "index.html" if sp == "" else f"{sp}.html"
        if not os.path.exists(expected_file):
            errors.append(f"sitemap.xml contains route '/{sp}' but '{expected_file}' does not exist on disk.")

    print(f"   Synced {len(urls)} sitemap routes against local pages.")


def check_asset_hygiene(referenced_assets):
    print(f"{BLUE}{BOLD}3. Checking Asset Hygiene & File Sizes...{RESET}")
    # Inspect assets directory
    if os.path.exists("assets"):
        for root, _, files in os.walk("assets"):
            for f in files:
                filepath = os.path.join(root, f)
                rel_path = os.path.relpath(filepath, ".").replace("\\", "/")
                size_kb = os.path.getsize(filepath) / 1024
                
                # Warn on large images > 500 KB for PageSpeed / Core Web Vitals
                if size_kb > 500:
                    warnings.append(f"Large image {rel_path} ({size_kb:.1f} KB) - consider optimizing/compressing to WebP.")

    # Check for unreferenced media in root directory
    for root_file in glob.glob("*.*"):
        if root_file.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg")):
            if root_file not in referenced_assets and f"assets/{root_file}" not in referenced_assets:
                warnings.append(f"Unreferenced media file in root: '{root_file}' ({os.path.getsize(root_file)/1024:.1f} KB). Move to assets/ or delete if unused.")


def main():
    print(f"\n{BOLD}========================================{RESET}")
    print(f"{BOLD}    Rlevel Site SDLC Health Check       {RESET}")
    print(f"{BOLD}========================================\n{RESET}")

    html_files, referenced_assets = check_html_files()
    check_sitemap(html_files)
    check_asset_hygiene(referenced_assets)

    print("\n----------------------------------------")
    print(f"{BOLD}Summary:{RESET}")

    if warnings:
        print(f"\n{YELLOW}{BOLD}Warnings ({len(warnings)}):{RESET}")
        for w in warnings:
            print(f"  {YELLOW}⚠ {w}{RESET}")

    if errors:
        print(f"\n{RED}{BOLD}Errors ({len(errors)}):{RESET}")
        for e in errors:
            print(f"  {RED}✖ {e}{RESET}")
        print(f"\n{RED}{BOLD}FAILED: Quality checks did not pass.{RESET}\n")
        sys.exit(1)
    else:
        print(f"\n{GREEN}{BOLD}PASSED: All critical quality checks passed cleanly!{RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
