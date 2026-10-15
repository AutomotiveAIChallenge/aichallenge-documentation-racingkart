#!/usr/bin/env python3
"""Check ja/en page consistency for the mkdocs-static-i18n docs tree.

Usage: python3 scripts/check_i18n.py [--docs-dir docs] [--strict] [--json]

The docs use mkdocs-static-i18n "suffix" mode: pages are named
`name.ja.md` / `name.en.md`. A file with no language suffix (e.g.
`name.md`) is shared by both languages and is not checked here, since
there is nothing to compare it against. Japanese is the default
language; the English site falls back to the Japanese page when no
`.en.md` file exists.

This is a standalone script, not a CI job. Run it by hand before
opening a PR that touches docs/. It uses only the Python standard
library.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

SUFFIX_RE = re.compile(r"^(?P<base>.+)\.(?P<lang>ja|en)\.md$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ANCHOR_RE = re.compile(r"\{\s*#([A-Za-z0-9_-]+)\s*\}\s*$")
IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
IMAGE_HTML_RE = re.compile(r"<img\b", re.IGNORECASE)
ADMONITION_RE = re.compile(r"^\s*(!!!|\?\?\?\+?)\s+\S")
FENCE_CHARS = ("`", "~")
MIN_FENCE_LEN = 3


@dataclass
class CodeBlock:
    info: str
    lines: list[str]


# Fence languages that are rendered diagrams rather than commands. Their
# visible text (node labels, etc.) is meant to be translated, so content
# drift here is expected and not a bug. They are still counted towards the
# code-block-count check, just excluded from the content-equality check.
DIAGRAM_FENCE_LANGS = {"mermaid"}


@dataclass
class ParsedPage:
    """A markdown page with fenced code removed from the prose view."""

    heading_levels: dict[int, int] = field(default_factory=dict)
    anchors: set[str] = field(default_factory=set)
    code_blocks: list[CodeBlock] = field(default_factory=list)
    image_count: int = 0
    admonition_count: int = 0


def split_fences(text: str) -> tuple[list[str], list[CodeBlock]]:
    """Return (non-fence lines, list of code blocks with their info string)."""
    lines = text.splitlines()
    non_fence_lines: list[str] = []
    code_blocks: list[CodeBlock] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_info = ""
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not in_fence:
            if len(stripped) >= MIN_FENCE_LEN and stripped[0] in FENCE_CHARS:
                run = len(stripped) - len(stripped.lstrip(stripped[0]))
                if run >= MIN_FENCE_LEN:
                    in_fence = True
                    fence_char = stripped[0]
                    fence_len = run
                    fence_info = stripped[run:].strip().lower()
                    current = []
                    continue
            non_fence_lines.append(line)
            continue
        # Inside a fence: look for a matching closing line.
        is_close = len(stripped) >= fence_len and set(stripped) == {fence_char}
        if is_close:
            in_fence = False
            code_blocks.append(CodeBlock(info=fence_info, lines=current))
            current = []
            continue
        current.append(line)
    if in_fence:
        # Unterminated fence: treat what we collected as a trailing block
        # rather than silently dropping it.
        code_blocks.append(CodeBlock(info=fence_info, lines=current))
    return non_fence_lines, code_blocks


def parse_page(text: str) -> ParsedPage:
    page = ParsedPage()
    non_fence_lines, code_blocks = split_fences(text)
    page.code_blocks = code_blocks
    for line in non_fence_lines:
        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            page.heading_levels[level] = page.heading_levels.get(level, 0) + 1
            anchor_match = ANCHOR_RE.search(heading_match.group(2))
            if anchor_match:
                page.anchors.add(anchor_match.group(1))
            continue
        if ADMONITION_RE.match(line):
            page.admonition_count += 1
        page.image_count += len(IMAGE_MD_RE.findall(line))
        page.image_count += len(IMAGE_HTML_RE.findall(line))
    return page


TRAILING_COMMENT_RE = re.compile(r"\s+#\s.*$")
JAPANESE_RE = re.compile(r"[぀-ヿ㐀-鿿]")


def strip_comment_lines(block: list[str]) -> str:
    """Drop comment-only lines and trailing ` # comment` parts, which may be translated."""
    kept = [line for line in block if not line.strip().startswith("#")]
    kept = [TRAILING_COMMENT_RE.sub("", line) for line in kept]
    return "\n".join(line.rstrip() for line in kept).strip()


def is_translatable_text(normalized: str) -> bool:
    """A block that still contains Japanese after removing comments is prose-like
    (a text diagram, a placeholder such as <hostのIP>), not a command to copy."""
    return bool(JAPANESE_RE.search(normalized))


@dataclass
class Finding:
    page: str
    category: str
    message_ja: str
    message_en: str
    detail: dict | None = None

    def to_dict(self) -> dict:
        result = {
            "page": self.page,
            "category": self.category,
            "message_ja": self.message_ja,
            "message_en": self.message_en,
        }
        if self.detail:
            result["detail"] = self.detail
        return result


def find_markdown_pairs(docs_dir: Path) -> tuple[dict[str, dict[str, Path]], list[Path]]:
    """Group suffixed markdown files by base key; also return shared files."""
    pairs: dict[str, dict[str, Path]] = {}
    shared: list[Path] = []
    for path in sorted(docs_dir.rglob("*.md")):
        rel = path.relative_to(docs_dir).as_posix()
        match = SUFFIX_RE.match(rel)
        if not match:
            shared.append(path)
            continue
        base = match.group("base")
        lang = match.group("lang")
        pairs.setdefault(base, {})[lang] = path
    return pairs, shared


def check_missing_counterparts(pairs: dict[str, dict[str, Path]]) -> Iterator[Finding]:
    for base, langs in sorted(pairs.items()):
        if "en" not in langs:
            yield Finding(
                page=base,
                category="missing_counterpart",
                message_ja=(
                    f"{base}.en.md がありません。英語サイトでは日本語版が代わりに表示されます。"
                ),
                message_en=(
                    f"{base}.en.md is missing. The English site will fall back to "
                    "showing the Japanese page."
                ),
            )
        if "ja" not in langs:
            yield Finding(
                page=base,
                category="missing_counterpart",
                message_ja=(
                    f"{base}.ja.md がありません。日本語がデフォルト言語のため、"
                    "日本語サイトにこのページが表示されない可能性があります。"
                ),
                message_en=(
                    f"{base}.ja.md is missing. Since Japanese is the default "
                    "language, this page may not appear on the Japanese site."
                ),
            )


def check_pair_drift(base: str, ja_page: ParsedPage, en_page: ParsedPage) -> Iterator[Finding]:
    ja_only_anchors = ja_page.anchors - en_page.anchors
    en_only_anchors = en_page.anchors - ja_page.anchors
    if ja_only_anchors or en_only_anchors:
        yield Finding(
            page=base,
            category="anchor_mismatch",
            message_ja=(
                "見出しアンカー {#id} が日本語版と英語版で一致していません。"
                "リンクが片方の言語で壊れる可能性があります。"
            ),
            message_en=(
                "Heading anchors {#id} do not match between the Japanese and "
                "English pages. Links may break on one language."
            ),
            detail={
                "ja_only": sorted(ja_only_anchors),
                "en_only": sorted(en_only_anchors),
            },
        )

    all_levels = sorted(set(ja_page.heading_levels) | set(en_page.heading_levels))
    level_diffs = {
        level: {"ja": ja_page.heading_levels.get(level, 0), "en": en_page.heading_levels.get(level, 0)}
        for level in all_levels
        if ja_page.heading_levels.get(level, 0) != en_page.heading_levels.get(level, 0)
    }
    if level_diffs:
        yield Finding(
            page=base,
            category="heading_count_mismatch",
            message_ja="見出しレベルごとの数が日本語版と英語版で異なります。",
            message_en="The number of headings per level differs between the "
            "Japanese and English pages.",
            detail=level_diffs,
        )

    ja_blocks = ja_page.code_blocks
    en_blocks = en_page.code_blocks
    if len(ja_blocks) != len(en_blocks):
        yield Finding(
            page=base,
            category="code_block_count_mismatch",
            message_ja=(
                f"コードブロックの数が異なります（日本語 {len(ja_blocks)} / 英語 {len(en_blocks)}）。"
            ),
            message_en=(
                f"The number of fenced code blocks differs (ja {len(ja_blocks)} "
                f"/ en {len(en_blocks)})."
            ),
        )
    else:
        for index, (ja_block, en_block) in enumerate(zip(ja_blocks, en_blocks)):
            if ja_block.info in DIAGRAM_FENCE_LANGS or en_block.info in DIAGRAM_FENCE_LANGS:
                # Diagram labels are supposed to be translated; comparing
                # their text as if it were a command would be a false
                # positive.
                continue
            ja_normalized = strip_comment_lines(ja_block.lines)
            en_normalized = strip_comment_lines(en_block.lines)
            if is_translatable_text(ja_normalized):
                continue
            if ja_normalized != en_normalized:
                yield Finding(
                    page=base,
                    category="code_block_content_mismatch",
                    message_ja=(
                        f"{index + 1} 番目のコードブロックの内容（コメント行を除く）が"
                        "日本語版と英語版で異なります。コマンドは両言語で同一である必要があります。"
                    ),
                    message_en=(
                        f"Fenced code block #{index + 1} differs between the "
                        "Japanese and English pages after stripping comment-only "
                        "lines. Commands should be identical across languages."
                    ),
                    detail={"ja": ja_normalized, "en": en_normalized},
                )

    if ja_page.image_count != en_page.image_count:
        yield Finding(
            page=base,
            category="image_count_mismatch",
            message_ja=(
                f"画像の数が異なります（日本語 {ja_page.image_count} / 英語 {en_page.image_count}）。"
            ),
            message_en=(
                f"The number of images differs (ja {ja_page.image_count} / "
                f"en {en_page.image_count})."
            ),
        )

    if ja_page.admonition_count != en_page.admonition_count:
        yield Finding(
            page=base,
            category="admonition_count_mismatch",
            message_ja=(
                "注釈ブロック（!!! / ???）の数が異なります"
                f"（日本語 {ja_page.admonition_count} / 英語 {en_page.admonition_count}）。"
            ),
            message_en=(
                "The number of admonitions (!!! / ???) differs (ja "
                f"{ja_page.admonition_count} / en {en_page.admonition_count})."
            ),
        )


def run_checks(docs_dir: Path) -> list[Finding]:
    pairs, _shared = find_markdown_pairs(docs_dir)
    findings: list[Finding] = list(check_missing_counterparts(pairs))
    for base, langs in sorted(pairs.items()):
        if "ja" not in langs or "en" not in langs:
            continue
        ja_text = langs["ja"].read_text(encoding="utf-8")
        en_text = langs["en"].read_text(encoding="utf-8")
        ja_page = parse_page(ja_text)
        en_page = parse_page(en_text)
        findings.extend(check_pair_drift(base, ja_page, en_page))
    return findings


def summarize(findings: list[Finding]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for finding in findings:
        summary[finding.category] = summary.get(finding.category, 0) + 1
    return summary


CATEGORY_LABELS = {
    "missing_counterpart": "対になるページがありません / Missing counterparts",
    "anchor_mismatch": "見出しアンカーの不一致 / Heading anchor mismatches",
    "heading_count_mismatch": "見出し数の不一致 / Heading count mismatches",
    "code_block_count_mismatch": "コードブロック数の不一致 / Code block count mismatches",
    "code_block_content_mismatch": "コードブロック内容の不一致 / Code block content mismatches",
    "image_count_mismatch": "画像数の不一致 / Image count mismatches",
    "admonition_count_mismatch": "注釈ブロック数の不一致 / Admonition count mismatches",
}


def render_report(findings: list[Finding]) -> str:
    lines: list[str] = []
    lines.append("ja/en ドキュメント整合性チェック / ja/en documentation consistency check")
    lines.append("=" * 70)
    if not findings:
        lines.append(
            "問題は見つかりませんでした。 / No issues were found."
        )
        return "\n".join(lines)

    by_page: dict[str, list[Finding]] = {}
    for finding in findings:
        by_page.setdefault(finding.page, []).append(finding)

    for page in sorted(by_page):
        lines.append("")
        lines.append(f"## {page}")
        for finding in by_page[page]:
            lines.append(f"- [{finding.category}] {finding.message_ja}")
            lines.append(f"  {finding.message_en}")
            if finding.detail:
                lines.append(f"  detail: {finding.detail}")

    lines.append("")
    lines.append("-" * 70)
    lines.append("まとめ / Summary")
    summary = summarize(findings)
    for category, count in sorted(summary.items()):
        label = CATEGORY_LABELS.get(category, category)
        lines.append(f"  {label}: {count}")
    lines.append(f"  合計 / Total: {len(findings)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check ja/en documentation consistency for mkdocs-static-i18n pages."
    )
    parser.add_argument("--docs-dir", default="docs", help="Path to the docs directory.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with status 1 if any issue is found (default: informational, exit 0).",
    )
    parser.add_argument(
        "--json", action="store_true", help="Print machine-readable JSON instead of text."
    )
    args = parser.parse_args(argv)

    docs_dir = Path(args.docs_dir)
    if not docs_dir.is_dir():
        print(f"docs dir not found: {docs_dir}", file=sys.stderr)
        return 2

    findings = run_checks(docs_dir)

    if args.json:
        payload = {
            "findings": [f.to_dict() for f in findings],
            "summary": summarize(findings),
            "total": len(findings),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_report(findings))

    if args.strict and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
