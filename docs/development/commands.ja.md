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
| `./docker_build.sh eval` | 提出ファイルを組み込んだ評価用イメージ（`aichallenge-2025-eval`）をビルドします（`--no-cache` で毎回フルビルド） |
| `./docker_build.sh eval --submit <path>` | 提出ファイルのパスを指定してビルドします（省略時: `submit/aichallenge_submit.tar.gz`） |

## make コマンド

### ビルド・起動・停止

| コマンド | 説明 |
|---|---|
| `make autoware-build` | ROSワークスペース（`aichallenge/workspace/`）をビルドします |
| `make dev` | AWSIM + Autoware を開発用に起動します（`simulator` + `autoware-simulator` の短縮形） |
| `make dev2` | AWSIM + Autoware x 2 を開発用に起動します |
| `make dev3` | AWSIM + Autoware x 3 を開発用に起動します |
| `make dev4` | AWSIM + Autoware x 4 を開発用に起動します |
| `make eval` | AWSIM + Autoware を評価用に起動します |
| `make gate1` | 安全ゲートシナリオ（障害物停止）を起動します |
| `make gate2` | 安全ゲートシナリオ（追い越し）を起動します |
| `make gate3` | 安全ゲートシナリオ（車線維持）を起動します |
| `make down` | 起動中のコンテナをすべて停止・削除します |
| `make down_all` | ホスト上の全Dockerコンテナを強制削除します |
| `make ps` | 起動中のコンテナ一覧を表示します |
| `make autoware-attach` | 既存コンテナのbashに入ります |
| `make autoware-bash` | 新規コンテナのbashに入ります |

### 個別サービスの起動

| コマンド | 説明 |
|---|---|
| `make simulator` | AWSIM のみ起動します |
| `make simulator-dev2` | AWSIM のみ起動します (2台走行用) |
| `make simulator-dev3` | AWSIM のみ起動します (3台走行用) |
| `make simulator-dev4` | AWSIM のみ起動します (4台走行用) |
| `make autoware-simulator` | Autoware のみ起動します（シミュレータ向け） |
| `make autoware-vehicle` | Autoware のみ起動します（実車向け） |
| `make driver` | 実車インターフェース（`racing_kart_interface`）を起動します |
| `make zenoh` | Zenoh（実車遠隔接続）を起動します |
| `make rviz2` | RViz2 を起動します |
| `make autoware-driver-zenoh` | `driver` + `autoware` + `zenoh` をまとめて起動します（実車向け） |

### コマンド送信

| コマンド | 説明 |
|---|---|
| `make autoware-request-control` | 自動走行の制御モードリクエストを送信します |
| `make autoware-request-initialpose` | 初期姿勢の設定リクエストを送信します |
| `make awsim-request-reset` | シミュレータをリセットします |
| `make awsim-request-start` | シミュレータに対してレース開始指示を送ります |

### その他

| コマンド | 説明 |
|---|---|
| `make download` | 提出データをダウンロードします（`SUBMISSION_ID=<id>` で指定可） |
