# AI講座

## 概要

本大会ではEnd to End AI部門を用意しています。本部門ではカメラ画像とLiDARデータを入力として、制御信号（あるいは軌道）を出力して自動運転を実現することが求められています。

本ページでは、参加者の皆様に基礎知識や開発のヒントを身につけていただくため、主要なAIアルゴリズムを紹介し、提供パッケージの使用方法を説明します。これらのサンプルを改造したり、参考にして新規ノードを実装したりしてください。

![ai_image](assets/ai_image.png)

## AI用パッケージ

下記に本大会で提供しているAI用パッケージ一覧を紹介します。Autowareと結合済みのパッケージは `control_method` の設定を切り替えることで実行可能です。また、モデルの学習用スクリプトも提供しているため、ご自身でモデルの改善も可能です。具体的な使い方は各モデルの使用方法をご参照ください。各アルゴリズムの詳細は [Algorithms](./ml_sample/algorithms.md) にまとめています。

| モデル名 | 入力センサー | 出力 | パッケージ名 | 説明 |
|---|---|---|---|---|
| TinyLidarNet | LiDAR | 制御信号 | tiny_lidar_net_controller | [使用方法](./ml_sample/tiny_lidar_net.md) |
| PilotNet | カメラ | 制御信号 | pilot_net_controller | [使用方法](./ml_sample/pilot_net.md) |
| Soft Actor-Critic (強化学習) | カメラ、車速 | 制御信号 | rl_train_controller | [使用方法](./ml_sample/soft_actor_critic.md) |
| VLM Planner | カメラ | 軌道 | --- | [使用方法](./ml_sample/vlm_setup.md) |
| VAD Planner | カメラ | 軌道 | --- | [使用方法](./ml_sample/vad_setup.md) |

### 注意

- VLM PlannerとVAD Plannerは2026年大会のAutowareには未結合です。使用するためにはご自身で2026年大会の環境に取り込む必要があります。設計・実装の詳細については [Sample ROS Node (VLM Planner)](./ml_sample/ai_sample_node_vlm.md)を参照してください。
