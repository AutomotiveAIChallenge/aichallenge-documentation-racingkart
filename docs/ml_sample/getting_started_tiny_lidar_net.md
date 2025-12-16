# Getting started: TinyLiDARNet

このドキュメントでは、TinyLiDARNetのsetup方法・実行方法について説明します。

## Setup

AI Challenge 2025のドキュメントに従って、

- [仮想環境のインストール](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/docker.html)
- [描画ありAWSIMの起動](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/requirements.html)
    - ただし、[こちらのAWSIM](https://tier4inc-my.sharepoint.com/personal/taiki_tanaka_tier4_jp/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Ftaiki%5Ftanaka%5Ftier4%5Fjp%2FDocuments%2FAutonomousAIChallengePractice2026%2FE2ESimSingleTest&viewid=f55f657e%2D78ea%2D41f1%2D8ceb%2Da70ac2d24bfc&ga=1)を使用してください。
    - AWSIMの配置については[こちらのページ](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/visible-simulation.html)を参考に、`aichallenge-2025/aichallenge/simulator`に配置してください。実行ファイルが`aichallenge-2025/aichallenge/simulator/AWSIM/AWSIM.x86_64`に存在していることを確認してください。
- [大会用リポジトリのビルド・実行](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/build-docker.html)

までを実施してください。

```sh
cd ~/aichallenge-2025
./docker_run.sh dev gpu
```

```sh
cd /aichallenge
./build_autoware.bash
./run_evaluation.bash rosbag
```

## TinyLiDARNetの学習手順

TinyLiDARNetの学習には、Autowareから取得したrosbagが必要です。このセクションでは、rosbagの取得方法から、TinyLiDARNetの学習・デプロイまでの手順を説明します。

### Step1. rosbagの取得

このStepでは、複数のTerminalを用います。

```sh
cd ~/aichallenge-2025;bash docker_exec.sh
```

をdocker環境の外で実行すれば、コンテナ内で複数のTerminalを開くことができます。3回繰り返して、合計4つのTerminalを開いてください。

#### Terminal 1: scan generation nodeの起動

```sh
source /opt/ros/humble/setup.bash
source /autoware/install/setup.bash
source /aichallenge/workspace/install/setup.bash
```

```sh
ros2 launch laserscan_generator laserscan_generator.launch.xml   use_sim_time:=true   csv_path:=$(ros2 pkg prefix laserscan_generator)/share/laserscan_generator/map/lane.csv
```

#### Terminal 2: AWSIMの起動

```sh
cd /aichallenge/;./run_simulator.bash
```

#### Terminal 3: autowareの起動

```sh
cd /aichallenge/;./run_autoware.bash awsim
```

[こちらのlink](https://autowarefoundation.github.io/autoware-documentation/main/demos/planning-sim/lane-driving/#2-set-an-initial-pose-for-the-ego-vehicle)を参考にし、initial poseを設定してください。

設定できたら、AWSIMの画面右上にあるControlボタンを押し、ManualからAutonomousに切り替えます。

<img src="../assets/tiny_lidar_net_awsim.png" alt="awsim" width="50%">

#### Terminal 4: rosbagの記録開始

```sh
cd /aichallenge/;./record_rosbag.bash
```

走行が終わったら、Ctrl+Cでrosbagの記録を停止します。記録されたrosbagは、`/aichallenge/rosbag2_autoware`に保存されます。rosbagはディレクトリ単位で管理されるものなので、この場合は`rosbag2_autoware`が一つの記録の単位となります（内部に.mcap形式のファイルが蓄積されていきます）。
ディレクトリの名称を`rosbag2_autoware_train_01`や`rosbag2_autoware_val_01`のように変更しておきましょう。

## Step2. Dataset conversion

rosbagを学習用datasetに変換します。

```sh
cd /aichallenge/python_workspace/tiny_lidar_net/
```

```sh
python3 /aichallenge/python_workspace/tiny_lidar_net/extract_data_from_bag.py --bags-dir /aichallenge/rosbag2_autoware_train_01/ --outdir /aichallenge/python_workspace/tiny_lidar_net/dataset/train/
```

以下のような出力が得られたら成功です。

```sh
[INFO] [PID:99328] Found 1 bags. Starting processing with 1 workers.
[INFO] [PID:99356] Saved rosbag2_autoware: 413 samples (Total: 0.13s)
[INFO] [PID:99328] All processing finished in 0.34 seconds.
```

trainだけでなく、validation setも変換しておきましょう。

```sh
python3 /aichallenge/python_workspace/tiny_lidar_net/extract_data_from_bag.py --bags-dir /output/20251211-163407/rosbag2_autoware_val_01/ --outdir /aichallenge/python_workspace/tiny_lidar_net/dataset/val/
```

## Step3. Model training

```sh
python3 /aichallenge/python_workspace/tiny_lidar_net/train.py
```

CPUで学習を回したい場合や、RTX 50 seriesなどを用いていて、CUDAがこの環境に対応していない場合は、以下を実行してください。

```sh
CUDA_VISIBLE_DEVICES="" python3 /aichallenge/python_workspace/tiny_lidar_net/train.py
```

## Step4. Model deployment

- `.pth`から`.npy`に変換します

```sh
python3 /aichallenge/python_workspace/tiny_lidar_net/convert_weight.py --ckpt /aichallenge/python_workspace/tiny_lidar_net/checkpoints/best_model.pth --output /aichallenge/python_workspace/tiny_lidar_net/weights/converted_weights.npy
```

以下のような出力が得られれば成功です。

```sh
✅ Loaded checkpoint: /aichallenge/python_workspace/tiny_lidar_net/checkpoints/best_model.pth
✅ Saved NumPy weights to: weights/converted_weights.npy
```

作成した`converted_weights.npy`を、ROS 2 package内のckptディレクトリに移動します。

```sh
mv /aichallenge/python_workspace/tiny_lidar_net/weights/converted_weights.npy /aichallenge/workspace/src/aichallenge_submit/tiny_lidar_net_controller/ckpt/tinylidarnet_weights.npy
```

## Step5. Run TinyLiDARNet Sample ROS Node

[`reference.launch.xml`におけるcontrol mode](https://github.com/AutomotiveAIChallenge/aichallenge-2025/blob/6706f4cb1bd3b1e50dc56e092ebd51ca174a3530/aichallenge/workspace/src/aichallenge_submit/aichallenge_submit_launch/launch/reference.launch.xml#L20)を、`rule_based`から`e2e`に変更しましょう。

### Terminal 1: AWSIMの起動

```sh
cd /aichallenge/;./run_simulator.bash
```

### Terminal 2: autowareの起動

```sh
cd /aichallenge/;./run_autoware.bash awsim
```

[こちらのlink](https://autowarefoundation.github.io/autoware-documentation/main/demos/planning-sim/lane-driving/#2-set-an-initial-pose-for-the-ego-vehicle)を参考にし、initial poseを設定してください。

設定できたら、AWSIMの画面右上にあるControlボタンを押し、ManualからAutonomousに切り替えます。

<img src="../assets/tiny_lidar_net_awsim.png" alt="awsim" width="50%">

## 発展的課題

上記の手順で、TinyLiDARNetを用いた、サーキットでの単独走行が可能です。

### Pitlane走行

TinyLiDARNetは、コース上での走行は可能ですが、Pitlaneのような狭いエリアでの走行は苦手です。発展的課題として、[PitlaneからスタートするAWSIM環境](https://tier4inc-my.sharepoint.com/personal/taiki_tanaka_tier4_jp/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Ftaiki%5Ftanaka%5Ftier4%5Fjp%2FDocuments%2FAutonomousAIChallenge%2FAWSIM%2Dfor%2DFinal&viewid=f55f657e%2D78ea%2D41f1%2D8ceb%2Da70ac2d24bfc&ga=1)を用いてPitlaneを含むrosbagを収集し、Pitlane走行が可能なTinyLiDARNetの学習に挑戦してみてください。

<img src="../assets/tiny_lidar_net_awsim_pitlane.png" alt="awsim" width="30%">

### アクセル制御の追加

現在のdefault設定では、TinyLiDARNetはステアリング制御のみを行い、[アクセルは固定値](https://github.com/AutomotiveAIChallenge/aichallenge-2025/blob/6706f4cb1bd3b1e50dc56e092ebd51ca174a3530/aichallenge/workspace/src/aichallenge_submit/tiny_lidar_net_controller/config/tiny_lidar_net_node.param.yaml#L12-L13)で制御しています。`control_mode: "ai"`に変更し、アクセル制御もTinyLiDARNetに実施させてみましょう。

### TinyLiDARNetでのOvertake

単独走行であれば、ML Plannerを用いる必要性は低いですが、複数台走行の場合は、overtakeといった高度な意思決定が必要となり、機械学習の活躍場面が増えます。[複数台走行用のAWSIM](https://tier4inc-my.sharepoint.com/personal/taiki_tanaka_tier4_jp/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Ftaiki%5Ftanaka%5Ftier4%5Fjp%2FDocuments%2FAutonomousAIChallengePractice2026%2FE2ESimPractice&viewid=f55f657e%2D78ea%2D41f1%2D8ceb%2Da70ac2d24bfc&ga=1)を使用すれば、複数台走行データを収集・学習することができます。

<img src="../assets/tiny_lidar_net_awsim_multi_car.png" alt="awsim" width="50%">

### 画像入力の追加

`use image`オプションをTrueにすることで、画像入力を追加することができます。TinyLiDARNetはLiDAR情報のみを用いていますが、この画像入力も使用したmodel,つまり**TinyLiDARImageNet**を実装すれば、LiDARだけでなく画像も考慮して走行することが期待されます。今後、信号や黄旗などが登場した際には、画像入力を検討してみてください。

<img src="../assets/camera_awsim_after.png" alt="awsim" width="50%">
