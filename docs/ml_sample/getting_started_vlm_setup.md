# Getting started: Setup for VLM Planner

このドキュメントでは、Gemini APIとAWSIMを用いて、VLM Plannerのsetupを行う方法について説明します。

## AWSIM側の準備

[aichallenge-2025-e2e-test](https://github.com/AutomotiveAIChallenge/aichallenge-2025-e2e-test)をcloneしてください。ここではホームディレクトリを指定していますが、お好きなディレクトリに配置していただいて構いません。

```sh
cd ~
git clone https://github.com/AutomotiveAIChallenge/aichallenge-2025-e2e-test
```

AI Challenge 2025のドキュメントに従って、

- [仮想環境のインストール](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/docker.html)
- [描画ありAWSIMの起動](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/requirements.html)
- [大会用リポジトリのビルド・実行](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/build-docker.html)

までを実施してください。

```sh
cd ~/aichallenge-2025-e2e-test
./docker_run.sh dev gpu
```

```sh
cd /aichallenge
./build_autoware.bash
./run_evaluation.bash
```

- AWSIMが表示されたら、AWSIMでuse imageのボタンを押してカメラ画像を有効にします。
- カメラ画像が左上に表示されれば、AWSIM用環境の準備はOKです。

![alt text](../assets/camera_awsim_after.png)

## Gemini APIの準備

- [こちらのdocument](https://ai.google.dev/gemini-api/docs/api-key?hl=ja)に従って、Gemini API KEYを取得してください。

!!! info

    Gemini API KEYは自分だけしか見られない場所に保管してください。GitHubにpushしないよう気をつけましょう。

## VLM Planner環境側の準備

### docker imageのpull


!!! info

    docker pullでは、10GB程度のlayerのdownloadを行います。通信環境によっては、一時間以上の実行時間が必要となります。

```sh
docker pull ghcr.io/autowarefoundation/autoware:universe-devel-cuda
```

### e2e_utils_betaの環境構築

[e2e_utils_beta](https://github.com/AutomotiveAIChallenge/e2e-utils-beta)をcloneしてください。

```sh
git clone https://github.com/AutomotiveAIChallenge/e2e-utils-beta.git
cd e2e_utils_beta
sh script/setup.sh
```

### docker run

- `/path/to/e2e_utils_beta`には、local環境にcloneしてきた`e2e_utils_beta`のpathを埋めてください。

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

- 以下の手順はdockerの中で実施してください。

```sh
cd /home/e2e_utils_beta
rosdep update;rosdep install -y --from-paths . --ignore-src --rosdistro $ROS_DISTRO
```

```sh
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Release --packages-up-to autoware_auto_planning_msgs autoware_internal_planning_msgs
```

### uvの環境構築

[こちら](https://docs.astral.sh/uv/getting-started/installation/)に従って`uv`をinstallしてください。


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

### Gemini APIの設定

- [Gemini APIの準備](#gemini-apiの準備)にて取得したAPI KEYを環境変数に設定しましょう。

```sh
export GEMINI_API_KEY="YOUR_API_KEY"
```

## Next Step

[Getting started: VLM Plannerの実行](./getting_started_vlm_run.md)へお進みください。
