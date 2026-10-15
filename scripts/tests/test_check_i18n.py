from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_i18n import parse_page, run_checks  # noqa: E402


class TestParsePage(unittest.TestCase):
    def test_heading_inside_code_fence_is_ignored(self) -> None:
        text = "\n".join(
            [
                "# Real heading",
                "```bash",
                "# not a heading, just a shell comment",
                "echo hi",
                "```",
            ]
        )
        page = parse_page(text)
        self.assertEqual(page.heading_levels, {1: 1})
        self.assertEqual(len(page.code_blocks), 1)

    def test_explicit_anchor_is_captured(self) -> None:
        text = "## Section { #my-anchor }"
        page = parse_page(text)
        self.assertEqual(page.anchors, {"my-anchor"})

    def test_images_and_admonitions_counted(self) -> None:
        text = "\n".join(
            [
                "![alt](a.png)",
                "<img src='b.png'>",
                "!!! note",
                "    body text",
            ]
        )
        page = parse_page(text)
        self.assertEqual(page.image_count, 2)
        self.assertEqual(page.admonition_count, 1)


class TestRunChecks(unittest.TestCase):
    def _write(self, root: Path, name: str, content: str) -> None:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_missing_counterpart_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(docs, "lonely.ja.md", "# Only Japanese\n")
            findings = run_checks(docs)
            categories = [f.category for f in findings]
            self.assertIn("missing_counterpart", categories)
            missing = [f for f in findings if f.category == "missing_counterpart"][0]
            self.assertEqual(missing.page, "lonely")

    def test_anchor_mismatch_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(docs, "page.ja.md", "## 見出し { #japanese-only }\n")
            self._write(docs, "page.en.md", "## Heading { #english-only }\n")
            findings = run_checks(docs)
            anchor_findings = [f for f in findings if f.category == "anchor_mismatch"]
            self.assertEqual(len(anchor_findings), 1)
            self.assertEqual(anchor_findings[0].detail["ja_only"], ["japanese-only"])
            self.assertEqual(anchor_findings[0].detail["en_only"], ["english-only"])

    def test_matching_anchors_produce_no_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(docs, "page.ja.md", "## 見出し { #shared-id }\n")
            self._write(docs, "page.en.md", "## Heading { #shared-id }\n")
            findings = run_checks(docs)
            self.assertEqual(findings, [])

    def test_code_block_differing_only_by_translated_comment_is_equal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(
                docs,
                "cmds.ja.md",
                "\n".join(["```bash", "# ビルドする", "make build", "```", ""]),
            )
            self._write(
                docs,
                "cmds.en.md",
                "\n".join(["```bash", "# build the project", "make build", "```", ""]),
            )
            findings = run_checks(docs)
            self.assertEqual(findings, [])

    def test_differing_command_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(
                docs,
                "cmds.ja.md",
                "\n".join(["```bash", "make build", "```", ""]),
            )
            self._write(
                docs,
                "cmds.en.md",
                "\n".join(["```bash", "make test", "```", ""]),
            )
            findings = run_checks(docs)
            content_findings = [f for f in findings if f.category == "code_block_content_mismatch"]
            self.assertEqual(len(content_findings), 1)
            self.assertEqual(content_findings[0].detail["ja"], "make build")
            self.assertEqual(content_findings[0].detail["en"], "make test")

    def test_mermaid_diagram_label_translation_is_not_a_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(
                docs,
                "diagram.ja.md",
                "\n".join(["```mermaid", "flowchart LR", "    A[開始] --> B[終了]", "```", ""]),
            )
            self._write(
                docs,
                "diagram.en.md",
                "\n".join(["```mermaid", "flowchart LR", "    A[Start] --> B[End]", "```", ""]),
            )
            findings = run_checks(docs)
            self.assertEqual(findings, [])

    def test_shared_unsuffixed_file_is_not_checked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(docs, "shared.md", "# Shared\n")
            findings = run_checks(docs)
            self.assertEqual(findings, [])

    def test_translated_trailing_comment_is_not_a_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(docs, "p.ja.md", "```bash\nsudo ufw allow 7777/udp   # ufw を使っている場合\n```\n")
            self._write(docs, "p.en.md", "```bash\nsudo ufw allow 7777/udp   # if you use ufw\n```\n")
            self.assertEqual(run_checks(docs), [])

    def test_block_with_japanese_text_is_treated_as_translatable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(docs, "p.ja.md", "```\nping <hostのIP>\n```\n")
            self._write(docs, "p.en.md", "```\nping <host IP>\n```\n")
            self.assertEqual(run_checks(docs), [])

    def test_changed_command_with_trailing_comment_is_still_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(docs, "p.ja.md", "```bash\ngit clone https://example.com/new.git  # 取得\n```\n")
            self._write(docs, "p.en.md", "```bash\ngit clone https://example.com/old.git  # fetch\n```\n")
            categories = {f.category for f in run_checks(docs)}
            self.assertEqual(categories, {"code_block_content_mismatch"})

    def test_heading_and_image_count_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write(docs, "p.ja.md", "# A\n## B\n![x](x.png)\n")
            self._write(docs, "p.en.md", "# A\n")
            findings = run_checks(docs)
            categories = {f.category for f in findings}
            self.assertIn("heading_count_mismatch", categories)
            self.assertIn("image_count_mismatch", categories)


if __name__ == "__main__":
    unittest.main()
