# 環境の説明

大会用リポジトリでは、ビルド・実行環境はすべて Docker コンテナ内で完結しています。
各コンテナは `docker-compose.yml` でサービスとして定義されており、参加者が日常的に使う操作は `make` コマンドでラップされています。そのため、Docker Compose の詳細を意識せずに開発を進められます。

Autoware構成の詳細については、[メインモジュール](main-module.ja.md)を参照してください。

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

## サービス一覧

`docker-compose.yml` で定義されているサービスの一覧です。

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

### aichallenge_submit の構成

参加者が変更できるパッケージが `aichallenge_submit/` にまとめられています。

| パッケージ | 概要 |
|---|---|
| `aichallenge_submit_launch/` | 起動設定・パラメータ・マップ・データを管理するランチパッケージ |
| `simple_pure_pursuit/` | Pure Pursuit ベースのルールベース制御 |
| `simple_trajectory_generator/` | 経路（Trajectory）生成 |
| `path_to_trajectory/` | Path メッセージを Trajectory に変換 |
| `multi_purpose_mpc_ros/` | MPC（モデル予測制御）ベースの制御 |
| `tiny_lidar_net_controller/` | TinyLiDARNet による End-to-End 制御 |
| `pilot_net_controller/` | PilotNet による End-to-End 制御 |
| `gyro_odometer/` | ジャイロセンサを使ったオドメトリ推定 |
| `imu_corrector/` | IMU データの補正 |
| `imu_gnss_poser/` | IMU と GNSS を組み合わせた位置推定 |
| `racing_kart_gnss_poser/` | レーシングカート向け GNSS 位置推定 |
| `laserscan_generator/` | 点群から LaserScan を生成 |
| `racing_kart_description/` | 車両モデル（URDF・メッシュ） |
| `racing_kart_sensor_kit_description/` | センサキット構成（URDF） |
