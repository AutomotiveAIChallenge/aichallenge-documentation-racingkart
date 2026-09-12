# 海外・日本語以外の参加者向けガイド

日本語を読まない参加チームのための入口のページです（英語版が本文です）。ドキュメントは日本語と英語で提供しており、英語版がないページは英語サイトでも日本語のページが表示されます。

## 最初に読むページ

1. [はじめに](./getting-started.ja.md): 大会の概要と始め方
2. [推奨環境](./setup/requirements.ja.md)と[環境構築](./setup/introduction.ja.md): 対応 OS は Ubuntu 22.04
3. 参加部門のルール: [Sim to Real SW部門](./competition/sw-class.ja.md) または [End to End AI部門](./competition/ai-class.ja.md)
4. [提出方法](./competition/submission.ja.md): アップロードとマッチメイキング
5. 決勝進出チーム: [SIM決勝](./competition/sim-finals.ja.md)、[SIM決勝 PC 環境説明](./competition/sim-finals-pc.ja.md)、[実機決勝](./competition/kart-finals.ja.md)

公式の日程とエントリー情報は [JSAE の大会ページ](https://www.jsae.or.jp/jaaic/index/overview/)にあります。

## 環境

- Ubuntu 22.04 を使ってください。Windows しかない場合は、[推奨環境](./setup/requirements.ja.md)のとおり、できれば別の SSD に Ubuntu をインストールしてください。
- GPU なし（AWSIM のヘッドレス実行）でも動かせますが、公式にはサポートされていません。

## 言葉について

- ルール、オンライン環境、Slack には日本語の用語が多く出てきます。[用語集](./glossary.ja.md)を参照してください。
- 英語版と日本語版の内容が食い違うように見えるときは、日本語版も確認し、質問チャンネルで聞いてください。
- 日本語ページはブラウザの翻訳で十分読めますが、コマンド・ファイル名・トピック名は書かれたとおりに使ってください。

## 質問するには

- [FAQ](./faq.ja.md)に、よくある質問と、FAQ にない質問の聞き方があります。
- 運営の Slack に質問チャンネルがあります。英語で書いて構いません。環境構築の質問では、環境と `./setup.bash doctor` の結果も添えてください。
- スターターキットの不具合は [aichallenge-racingkart](https://github.com/AutomotiveAIChallenge/aichallenge-racingkart) の Issue でも報告できます。
