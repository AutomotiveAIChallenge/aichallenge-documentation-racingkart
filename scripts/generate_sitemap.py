#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from xml.etree.ElementTree import Element, ElementTree, SubElement

from mkdocs.config import load_config


def iter_html_pages(site_dir: Path) -> Iterable[tuple[str, Path]]:
    for path in site_dir.rglob("*.html"):
        relative = path.relative_to(site_dir).as_posix()
        if relative == "404.html":
            continue
        yield relative, path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate sitemap.xml for a MkDocs site.")
    parser.add_argument("--config-file", default="mkdocs.yaml")
    parser.add_argument("--site-dir", default="site")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    config = load_config(config_file=args.config_file)
    site_url = (config.get("site_url") or "").strip()
    if not site_url:
        raise SystemExit("mkdocs.yaml must set site_url to generate sitemap.xml")
    if not site_url.endswith("/"):
        site_url += "/"

    site_dir = Path(args.site_dir)
    if not site_dir.is_dir():
        raise SystemExit(f"site dir not found: {site_dir}")

    output_path = Path(args.output) if args.output else site_dir / "sitemap.xml"

    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    entries = sorted(iter_html_pages(site_dir), key=lambda x: x[0])
    for relative, path in entries:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = f"{site_url}{relative}"
        lastmod = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).date()
        SubElement(url, "lastmod").text = lastmod.isoformat()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    ElementTree(urlset).write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

