# ドキュメント構成ガイド

このページは、`docs/` 配下の配置ルールと、ページ追加・構成変更の手順をまとめたものです。

## 基本方針

- 参加者の導線（読む順）を優先して `nav` を設計する
- URL を極力変えない（移動・改名が必要な場合はリダイレクトも用意する）
- 多言語は `mkdocs-static-i18n` の suffix 方式を使う（`.ja.md` / `.en.md`）
- 公開しない下書きは `docs/` へ置かず、`drafts/` に置く

## 置き場所（目安）

- 競技概要: `docs/index.*.md`
- はじめに: `docs/getting-started.*.md`
- 予選: `docs/preliminaries/`
- 決勝: `docs/finals/`
- 環境構築: `docs/setup/`
- 開発: `docs/development/`
- 仕様: `docs/specifications/`
- 入門講座: `docs/course/`
- AI講座: `docs/ai.*.md` と `docs/ml_sample/`
- FAQ/コミュニティ: `docs/faq.*.md`, `docs/community.*.md`
- 議論中の項目: `docs/discussions.*.md`

## 新しいページを追加する手順

1. `docs/<path>.ja.md` / `docs/<path>.en.md` を作成する
2. `mkdocs.yaml` の `nav:` に `<path>.md`（suffix無し）を追加する
3. 見出し名を日本語側で上書きしたい場合は、`mkdocs.yaml` の `nav_translations` を更新する
4. `mkdocs build` でリンク切れ・警告がないか確認する
