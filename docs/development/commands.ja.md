# コマンド一覧

## setup.bash

環境チェックや初期セットアップを行います。

| コマンド | 説明 |
|---|---|
| `./setup.bash` | 環境チェックと次のステップを表示します（`doctor` と同じ） |
| `./setup.bash doctor` | 環境チェックと次のステップのサマリーを表示します |
| `./setup.bash bootstrap` | Docker のインストール・リポジトリのクローン・セットアップを一括実行します（新規PCのセットアップ用） |
| `./setup.bash pull image` | Autoware ベースイメージを `docker pull` します |
| `./setup.bash download awsim` | AWSIM.zip をダウンロードして展開します |
| `./setup.bash env` | `.env.example` から `.env` を作成します |

## create_submit_file.bash

`aichallenge_submit/` を圧縮して提出ファイルを作成します。出力先は `submit/aichallenge_submit.tar.gz` です。

```bash
./create_submit_file.bash
```

## docker_build.sh

Dockerイメージをビルドします。ビルドログは `output/docker/` 配下に保存されます。

| コマンド | 説明 |
|---|---|
| `./docker_build.sh dev` | 開発用イメージ（`aichallenge-2025-dev`）をビルドします |
| `./docker_build.sh eval` | 評価用イメージ（`aichallenge-2025-eval`）をビルドします（`--no-cache` で毎回フルビルド） |
| `./docker_build.sh eval --submit <path>` | 提出ファイルを組み込んだ評価用イメージをビルドします |

## run_parallel_submissions.bash

複数の提出ファイルを同時に評価します。1〜4 つの提出ファイル（`aichallenge_submit.tar.gz`）を受け取り、それぞれ別の Domain ID（`d1`〜`d4`）で並列走行させます。

| コマンド | 説明 |
|---|---|
| `./run_parallel_submissions.bash --submit <tar1> [<tar2> ...]` | 1〜4 つの提出ファイルを並列評価します |
| `./run_parallel_submissions.bash down` | 起動中のコンテナをすべて停止します |

実行ログと結果は `output/<実行日時>/d<domain_id>/` 配下に保存されます。

## make コマンド

### ビルド・起動・停止

| コマンド | 説明 |
|---|---|
| `make autoware-build` | ROSワークスペース（`aichallenge/workspace/`）をビルドします |
| `make dev` | AWSIM + Autoware を開発用に起動します（`simulator` + `autoware-simulator` の短縮形） |
| `make eval` | AWSIM + Autoware を評価用に起動します |
| `make down` | 起動中のコンテナをすべて停止・削除します |
| `make down_all` | ホスト上の全Dockerコンテナを強制削除します |
| `make ps` | 起動中のコンテナ一覧を表示します |

### 個別サービスの起動

| コマンド | 説明 |
|---|---|
| `make simulator` | AWSIM のみ起動します |
| `make autoware-simulator` | Autoware のみ起動します（シミュレータ向け） |
| `make autoware-vehicle` | Autoware のみ起動します（実車向け） |
| `make driver` | 実車インターフェース（`racing_kart_interface`）を起動します |
| `make zenoh` | Zenoh（実車遠隔接続）を起動します |
| `make rviz2` | RViz2 を起動します |
| `make autoware-driver-zenoh` | `driver` + `autoware` + `zenoh` をまとめて起動します（実車向け） |

### コマンド送信

| コマンド | 説明 |
|---|---|
| `make autoware-request-initialpose` | 初期姿勢の設定リクエストを送信します |
| `make autoware-request-control` | 自動走行の制御モードリクエストを送信します |
| `make simulator-reset` | シミュレータをリセットします |

### その他

| コマンド | 説明 |
|---|---|
| `make download` | 提出データをダウンロードします（`SUBMISSION_ID=<id>` で指定可） |
