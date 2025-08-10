# Getting started

このドキュメントでは，Gemini APIとAWSIMを用いて，VLM Plannerを動かす方法について説明します．

## AWSIM側の準備

[環境構築](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/requirements.html)のドキュメントに従い，[描画ありAWSIMの起動](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/requirements.html)と[大会用リポジトリのビルド・実行](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/build-docker.html)までを実施してください．

```sh
cd ~/aichallenge-2025
./docker_run.sh dev gpu
```

```sh
cd /aichallenge
./build_autoware.bash
./run_evaluation.bash
```


AWSIMが表示されたら，AWSIMでuse imageのボタンを押してカメラ画像を有効にします．

![alt text](../assets/camera_awsim.png)

scaleは0.20程度に変更しましょう．(Geminiが5秒に1回しか推論できないため．)

## VLM Planner環境側の準備

### docker imageのpull


!!! info

    docker pullでは，10GB程度のlayerのdownloadを行います．通信環境によっては，一時間以上の実行時間が必要となります．

```sh
docker pull ghcr.io/autowarefoundation/autoware:universe-devel-cuda
```

### e2e_utils_betaの環境構築

[e2e_utils_beta](https://github.com/Shin-kyoto/e2e_utils_beta/tree/main)をcloneしてください．

```sh
git clone https://github.com/Shin-kyoto/e2e_utils_beta.git
cd e2e_utils_beta
sh script/setup.sh
```

### docker run

- `/path/to/e2e_utils_beta`には，local環境にcloneしてきた`e2e_utils_beta`のpathを埋めてください．

```sh
rocker \
  --nvidia \
  --x11 \
  --network host \
  --user \
  --volume /path/to/e2e_utils_beta:/home/e2e_utils_beta \
  --name aichallenge-e2e-utils \
  ghcr.io/autowarefoundation/autoware:universe-devel-cuda \
  /bin/bash
```

### colcon build

- 以下の手順はdockerの中で実施してください．

```sh
cd /home/e2e_utils_beta
rosdep update;rosdep install -y --from-paths . --ignore-src --rosdistro $ROS_DISTRO
```

```sh
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Release --packages-up-to autoware_auto_planning_msgs autoware_internal_planning_msgs
```

### uvの環境構築

[こちら](https://docs.astral.sh/uv/getting-started/installation/)に従って`uv`をinstallしてください．


```sh
cd e2e-utils-beta;source install/setup.bash
```

```sh
cd src/vlm_planner;uv venv -p python3.10
```

```sh
source .venv/bin/activate
```

```sh
uv pip install .
```

### Gemini APIの取得

- [こちらのdocument](https://ai.google.dev/gemini-api/docs/api-key?hl=ja)に従って，Gemini APIを取得してください．
- 取得したAPI KEYを環境変数に設定しましょう．

```sh
export GEMINI_API_KEY="YOUR_API_KEY"
```

## VLM Plannerの実行

- 以下のコマンドを実行し，VLM Plannerを動かしてみてください．

```sh
# Run the VLM planner node with custom output topic
cd e2e-utils-beta/src/vlm_planner
python vlm_planner_node.py --ros-args -p output_topic:="/planning/ml_planner/auto/trajectory"
```

以下のコマンドで出力が得られていれば，正しく実行できています．

```sh
ros2 topic echo /planning/ml_planner/auto/trajectory
```

## Tips

このSampleでは，`gemini-2.5-flash-lite`をそのまま使用しており，サーキット用のチューニングができておらず，ヘアピンを回ることができない状態です．以下のTipsを参考に，改善にトライしてみてください．

- `e2e-utils-beta/src/vlm_planner/vlm_planner.py`を更新することでモデルを変更できます
    - デフォルトでは`gemini-2.5-flash-lite`が使用されています．

```python
self.model = genai.GenerativeModel("gemini-2.5-flash-lite")
```

- プロンプト(e2e-utils-beta/src/vlm_planner/prompt.py)を更新することでも改善ができる可能性があります．

- [Vertex AIでのファインチューニング](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-use-supervised-tuning?hl=ja)が軌道の改善に役立つ可能性があります．

