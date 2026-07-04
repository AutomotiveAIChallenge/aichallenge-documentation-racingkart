# 環境の説明

大会用リポジトリでは、ビルド・実行環境はすべて Docker コンテナ内で完結しています。
各コンテナは `docker-compose.yml` でサービスとして定義されており、参加者が日常的に使う操作は `make` コマンドでラップされています。そのため、Docker Compose の詳細を意識せずに開発を進められます。

参加者が編集するパッケージ群は `aichallenge_submit/` です。詳細は[Autowareの構成](main-module.ja.md)を参照してください。

## ディレクトリ構成

```text
aichallenge-racingkart/
├── aichallenge/
│   ├── workspace/                            # ROS 2 ワークスペース
│   │   └── src/
│   │       ├── aichallenge_submit/           # ← 参加者が編集するパッケージ群
│   │       ├── aichallenge_system/           # 大会システムパッケージ（編集不要）
│   │       └── aichallenge_tools/            # ツール系パッケージ（編集不要）
│   ├── simulator/AWSIM/                      # AWSIM バイナリ
│   ├── ml_workspace/                         # 機械学習ワークスペース
│   └── utils/                                # ユーティリティスクリプト
├── output/                                   # 実行結果の出力先
├── submit/                                   # 提出用ファイル（create_submit_file.bash で生成）
├── docker-compose.yml                        # サービス定義
├── Makefile                                  # make コマンドのラッパー
└── docker_build.sh                           # Docker イメージビルドスクリプト
```

`make dev` 実行時、 `aichallenge/workspace/` と `output/` はコンテナにマウントされるため、ホスト側での編集内容や実行結果にコンテナ内から直接アクセスできます。

## Docker Compose サービス一覧

`docker-compose.yml` で定義されている Docker Compose サービスの一覧です（ROS 2 のサービスとは異なります）。

| サービス名 | 対応する make コマンド | 説明 |
|---|---|---|
| `autoware-build` | `make autoware-build` | ROS ワークスペースをビルドします |
| `simulator` | `make dev` / `make simulator` | AWSIM を起動します |
| `autoware` | `make dev` / `make autoware-simulator` / `make autoware-vehicle` | Autoware を起動します（`RUN_MODE` でシミュレータ向け／実車向けを切り替え） |
| `autoware-simulator-evaluation` | `make eval` | 評価用に AWSIM + Autoware を起動し、走行完了後に自動終了します |
| `autoware-command` | — | Autoware コンテナ内で任意のコマンドを実行します（ROS サービス呼び出しなど） |
| `zenoh` | `make zenoh` | 実車との遠隔接続に使う Zenoh ブリッジを起動します |
| `driver` | `make driver` | 実車インターフェース（`racing_kart_interface`）を起動します |
| `rviz2` | `make rviz2` | リモート可視化用の RViz2 を起動します |

## ワークスペースの構成

参考までに本大会で使用しているワークスペースの構成は以下となります。

!!! warning
    大会で提出するフォルダは `/aichallenge/workspace/src/aichallenge_submit` になります。このフォルダ以外で実装を追加・変更しても、提出物に含めることはできません。

### 開発環境（docker-dev）

![dev](./images/docker/dev.drawio.svg)

### 評価環境（docker-eval）

![eval](./images/docker/eval.drawio.svg)
