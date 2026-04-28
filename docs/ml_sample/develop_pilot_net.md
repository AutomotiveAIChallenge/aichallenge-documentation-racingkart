# Develop: PilotNet (Camera-based End-to-End)

このドキュメントでは、NVIDIA PilotNet (DAVE-2) を AI Challenge 環境で学習・デプロイする手順を説明します。tiny_lidar_net の手順を camera ベースに置き換えた形になっています。

- 参考論文: [End to End Learning for Self-Driving Cars (Bojarski et al., 2016)](https://arxiv.org/abs/1604.07316)
- アルゴリズムの位置付け: [ml_sample/algorithms.md](algorithms.md)
- ROS 推論ノード: [pilot_net_controller](https://github.com/AutomotiveAIChallenge/aichallenge-racingkart/tree/main/aichallenge/workspace/src/aichallenge_submit/pilot_net_controller)

tiny_lidar_net との主な違い:

| | tiny_lidar_net | pilot_net |
|---|---|---|
| 入力 | 2D LiDAR スキャン | フロントカメラ画像 (66x200) |
| 教師 | Autoware の経路追従コマンド | MPC エキスパートの制御コマンド |
| 推論 | NumPy | NumPy |
| 入力前処理 | 距離正規化 | 上部 37.5% クロップ → 66x200 リサイズ → YUV 変換 |

## Setup

AI Challenge のドキュメントに従って、

- [仮想環境のインストール](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/setup/docker.html)
- [描画あり AWSIM の起動](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/setup/requirements.html)
- [大会用リポジトリのビルド・実行](https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/setup/build-docker.html)

までを実施してください。

## PilotNet の学習手順

PilotNet の学習には Autoware から取得した rosbag が必要です。本セクションでは、rosbag の取得から学習・デプロイまでの手順を説明します。

### Step 1. コンテナの操作 (rocker で起動)

このステップでは、4 つの Terminal を使います。1つ目は **rocker で新しいコンテナを起動**し、残りは **既存コンテナに `docker exec` で入る**運用です。

#### rocker と docker_run.sh の関係

`./docker_run.sh dev` は内部で `rocker` を呼び出し、X11 / GPU (NVIDIA) / `/dev/dri` / `/dev/input` / PulseAudio / host network 等を passthrough した状態で開発用コンテナ (`aichallenge-2025-dev` イメージ) を起動します。`/aichallenge` がホストの作業ディレクトリに bind mount されるため、ホスト側で編集したコードが即座にコンテナから見えます。

実行されるコマンドは概ね次の形:

```sh
rocker --x11 --devices /dev/dri --user --pulse --net host --privileged \
    --name "aichallenge-2025-<timestamp>" \
    --volume "<volumes>" \
    -- aichallenge-2025-dev bash
```

GPU が検出されると `--nvidia` が自動付与されます (`./docker_run.sh dev gpu` で強制指定可)。

> **Note**: 競技用の `make dev` (docker compose) と異なり、`docker_run.sh dev` は GUI / USB アクセスが必要な開発・データ収集用フローです。本ドキュメントは後者を使います。

#### Terminal 1: AWSIM の起動 (rocker でコンテナ起動)

ホスト側で:

```sh
cd ~/aichallenge-racingkart
./docker_run.sh dev
```

`rocker` がコンテナを起動し、コンテナ内の bash に入ります。続けてコンテナ内で:

```sh
source /opt/ros/humble/setup.bash
source /autoware/install/setup.bash
source /aichallenge/workspace/install/setup.bash
./run_simulator.bash
```

PilotNet は単独走行を前提に動作確認するため、起動画面では **1人プレイ** を選択してください。

#### 追加 Terminal の開き方 (Terminal 2-4)

ホスト側で別の Terminal を開き (`Alt+Ctrl+T` 等)、すでに起動している rocker コンテナに `docker exec` で入ります:

```sh
cd ~/aichallenge-racingkart
./docker_exec.sh
```

`docker_exec.sh` は実行中の `aichallenge-2025-*` コンテナを検出し、`docker exec -it <container> bash` で同じコンテナの追加シェルを開きます。Terminal 2-4 ではこちらを使ってください (rocker をもう1度叩くと別コンテナになり、`/aichallenge` が同じでも IPC が分かれてしまうので非推奨)。

各 Terminal でも ROS 2 の source を実行します:

```sh
source /opt/ros/humble/setup.bash
source /autoware/install/setup.bash
source /aichallenge/workspace/install/setup.bash
```

#### Terminal 2: Autoware1 の起動

Terminal 2 (`docker_exec.sh` で入った状態) で:

```sh
./run_autoware.bash awsim 1
```

Initial pose を設定します。Rviz の view を `ThirdPersonFollower` から `TopdownOrtho` に切り替えてから設定してください。

設定したら、AWSIM 画面右上の Control ボタンで Manual → Autonomous に切り替えます。

#### Terminal 3: ROS topic の確認 (任意)

Terminal 3 (`docker_exec.sh` で入った状態) で:

```sh
export ROS_DOMAIN_ID=1
ros2 topic list
```

`/sensing/camera/image_raw` と `/control/command/control_cmd` の双方が存在することを確認してください。

#### Terminal 4: rosbag の記録開始

Terminal 4 (`docker_exec.sh` で入った状態) で:

```sh
export ROS_DOMAIN_ID=1
cd /aichallenge/ml_workspace
./record_data.bash
```

`record_data.bash` は `/sensing/camera/image_raw` と `/control/command/control_cmd` を含む形で `record_data.bash` 内に定義されているので、tiny_lidar_net と同じスクリプトでカメラデータも収集できます。

走行が終わったら Ctrl+C で記録を停止します。記録された rosbag は `/aichallenge/ml_workspace/rawdata/$(date +%Y%m%d-%H%M%S)` に保存されます。

検証データを別に取るのが理想ですが、まずは動作を掴むために訓練・検証ともに同じデータを使います:

```sh
cp -r /aichallenge/ml_workspace/rawdata/* /aichallenge/ml_workspace/train
```

```sh
cp -r /aichallenge/ml_workspace/rawdata/* /aichallenge/ml_workspace/val
```

<details>
<summary>※ teleop で手動収集する場合</summary>

Terminal 2 で `./run_autoware.bash awsim 1` の代わりに

```sh
export ROS_DOMAIN_ID=1
ros2 launch teleop_manager teleop_manager.launch.xml
```

を実行すると、Joycon 等で手動走行できます。
</details>

### Step 2. Dataset conversion

rosbag を学習用 dataset に変換します。

```sh
cd /aichallenge/ml_workspace/pilot_net/
```

```sh
python3 extract_data_from_bag.py \
    --bags-dir /aichallenge/ml_workspace/train/ \
    --outdir ./dataset/all/
```

このコマンドは内部で以下を実行します:

1. rosbag から `/sensing/camera/image_raw` と `/control/command/control_cmd` を時刻同期して取得
2. 各画像の上部 37.5% をクロップ (空・遠景を除外)
3. 66x200 にリサイズして `images.npy` (uint8) として保存
4. ステアリングと加速度を `steers.npy` / `accelerations.npy` に保存

以下のような出力が得られたら成功です:

```sh
[INFO] [PID:99328] Found 1 bags. Starting processing with 1 workers.
[INFO] [PID:99356] Saved rosbag2_autoware: 413 samples (Total: 0.13s)
[INFO] [PID:99328] All processing finished in 0.34 seconds.
```

続いて train/val 分割と水平反転 augmentation を行います:

```sh
python3 prepare_data.py
```

`dataset/train/merged/` と `dataset/val/merged/` が生成されます。

### Step 3. Model training

```sh
python3 train.py
```

CPU で学習を回したい場合や、RTX 50 シリーズなどで CUDA がこの環境に対応していない場合は次を実行してください:

```sh
CUDA_VISIBLE_DEVICES="" python3 train.py
```

学習ログ (TensorBoard) は `logs/` 配下、checkpoint は `checkpoints/` 配下に保存されます。`best_model.pth` が val loss 最良のモデルです。

ステアのみ学習したい場合 (アクセル学習が不安定なときに推奨):

```sh
python3 train.py train.loss.accel_weight=0.0
```

### Step 4. Model deployment

`.pth` から `.npy` に変換します:

```sh
python3 convert_weight.py \
    --ckpt /aichallenge/ml_workspace/pilot_net/checkpoints/best_model.pth \
    --output /aichallenge/ml_workspace/pilot_net/weights/pilotnet_weights.npy
```

以下のような出力が得られれば成功です:

```sh
Loaded checkpoint: /aichallenge/ml_workspace/pilot_net/checkpoints/best_model.pth
Saved NumPy weights to: /aichallenge/ml_workspace/pilot_net/weights/pilotnet_weights.npy
```

作成した `pilotnet_weights.npy` を ROS 2 package 内の ckpt ディレクトリにコピーします:

```sh
cp /aichallenge/ml_workspace/pilot_net/weights/pilotnet_weights.npy \
   /aichallenge/workspace/src/aichallenge_submit/pilot_net_controller/ckpt/pilotnet_weights.npy
```

### Step 5. Run PilotNet Sample ROS Node

`reference.launch.xml` の `control_method` を `rule_based` から `pilot_net` に変更します。

Step 1 でコンテナを既に起動している場合は、そのまま Terminal を再利用できます。コンテナを停止していた場合はホスト側で再度 `./docker_run.sh dev` (Terminal 1) と `./docker_exec.sh` (Terminal 2 以降) で入り直してください。

#### Terminal 1: AWSIM の起動

コンテナ内で:

```sh
source /opt/ros/humble/setup.bash
source /autoware/install/setup.bash
source /aichallenge/workspace/install/setup.bash
./run_simulator.bash
```

#### Terminal 2: Autoware1 の起動

別の Terminal (`docker_exec.sh` で入った状態) で:

```sh
source /opt/ros/humble/setup.bash
source /autoware/install/setup.bash
source /aichallenge/workspace/install/setup.bash
./run_autoware.bash awsim 1
```

[こちらのリンク](https://autowarefoundation.github.io/autoware-documentation/main/demos/planning-sim/lane-driving/#2-set-an-initial-pose-for-the-ego-vehicle) を参考に initial pose を設定してください。

設定できたら、AWSIM 画面右上の Control ボタンを押し、Manual から Autonomous に切り替えます。

## アクセル制御の追加

`pilot_net_node.param.yaml` の `control_mode` をデフォルトでは `"ai"` にしています。`"fixed"` に変更すると、ステアのみネットワークが推論し、アクセルは `acceleration` パラメータで指定した固定値を使います。

| `control_mode` | アクセル | ステアリング |
|---|---|---|
| `ai` | NN 出力 | NN 出力 |
| `fixed` | `acceleration` パラメータ (固定値) | NN 出力 |

`output_dim=1` で学習した場合 (ステアのみ学習) は自動的に `fixed` 相当の動作になります。

## ワンショット実行 (run_pipeline.bash)

extract → prepare → train → convert を一気に実行できます:

```sh
cd /aichallenge/ml_workspace/pilot_net
./run_pipeline.bash /aichallenge/ml_workspace/train
```

引数で解像度・色空間・出力次元・クロップ比率を変更できます:

```sh
./run_pipeline.bash <bag_dir> <image_height> <image_width> <color_space> <output_dim> <crop_top_ratio>
```

例: ステアのみ (output_dim=1):

```sh
./run_pipeline.bash /aichallenge/ml_workspace/train 66 200 yuv 1 0.375
```

## Notes

- **入力解像度を変える場合は学習側 (`run_pipeline.bash` の引数 または `train.yaml`) と推論側 (`pilot_net_node.param.yaml`) を必ず揃えてください。** ずらすと flatten dim 不一致でモデルが読めません。
- 複数台走行データの収集・学習は将来拡張です。詳細は [tiny_lidar_net の Overtake セクション](develop_tiny_lidar_net.md#tinylidarnetでのovertake) を参照。
- Rviz で camera topic を表示する場合は QoS を Reliable から BestEffort に変更してください。
- 推論性能: 66x200 でも 40Hz は CPU 推論で厳しい場合があります。必要なら ONNX Runtime への移行を検討してください。
