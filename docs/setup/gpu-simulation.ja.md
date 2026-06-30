# GPUの設定・動作設定

まず [環境構築の流れ](./introduction.ja.md) に沿ってセットアップを進めてください。AWSIMの描画やGPUの設定に問題が生じた場合は、本ページを参照してください。
また、Camera/LiDARはデフォルト無効です。AI 部門に参加する場合は[Camera/LiDAR設定の切り替え](#camera-lidar)の手順を参考にして設定してください。

## .envの確認 { #env-check }

`~/aichallenge-racingkart/.env` を確認して、以下の設定になっていることを確認します。本設定は `setup.bash` で自動的に行われます。`setup.bash` が `/dev/nvidia0` を検出した場合、`.env` の `COMPOSE_FILE` が自動的に設定されます。

もし NVIDIA GPU を使用しているにも関わらず設定が異なる場合は、後述のNVIDIA GPU 用の設定をしてから `.env` を更新してください。

```bash
# ご自身の環境に合う行を有効にして、他の行はコメントアウトしてください

# Intel 内蔵 GPU のみの場合・GPU未搭載の場合
COMPOSE_FILE=docker-compose.yml

# NVIDIA GPU 利用時
# COMPOSE_FILE=docker-compose.yml:docker-compose.gpu.yml:docker-compose.sound.yml
```

## GPUドライバなどのインストール

**全環境共通（NVIDIA GPU・Intel 内蔵 GPU）：**

- Vulkan導入

**NVIDIA GPU のみ：**

- NVIDIAドライバ導入（原則再起動推奨）
- NVIDIA Container Toolkit導入

??? note "Vulkanのインストール手順"
    以下のコマンドを実行します。

    ```bash
    sudo apt update
    sudo apt install -y libvulkan1
    ```

??? note "NVIDIAドライバのインストール手順"
    ```bash
    # リポジトリの追加
    sudo add-apt-repository ppa:graphics-drivers/ppa

    # パッケージリストの更新
    sudo apt update

    # インストール
    sudo ubuntu-drivers install

    # パッケージリストの更新
    sudo apt update

    # 下記のコマンドでインストールできていることを確認
    # 99%反映されないので、下記のrebootコマンドで再起動することを推奨します。
    nvidia-smi
    ```

    下記のコマンドでPCを再起動しますので、このタイミングで電源を落としたくない方は注意！
    ```bash
    # 再起動
    reboot
    ```

    ```bash
    # 再起動の後、インストールできていることを確認
    nvidia-smi
    ```

    ![nvidia-smi](./images/nvidia-smi.png)

??? note "NVIDIA Container Toolkit のインストール手順"
    NVIDIA Container Toolkit の公式手順
    （`https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html`）
    を参考にインストールを行います。

    ```bash
    # インストールの下準備
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
          && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
          && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
                sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
                sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    # インストール
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker

    # インストールできているかをテスト
    sudo docker run --rm --runtime=nvidia --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi

    # 最後のコマンドで以下のように出力されれば成功です。
    # （下記はNVIDIAウェブサイトからの引用です）
    #
    # +-----------------------------------------------------------------------------+
    # | NVIDIA-SMI 450.51.06    Driver Version: 450.51.06    CUDA Version: 11.0     |
    # |-------------------------------+----------------------+----------------------+
    # | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    # | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    # |                               |                      |               MIG M. |
    # |===============================+======================+======================|
    # |   0  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
    # | N/A   34C    P8     9W /  70W |      0MiB / 15109MiB |      0%      Default |
    # |                               |                      |                  N/A |
    # +-------------------------------+----------------------+----------------------+
    # +-----------------------------------------------------------------------------+
    # | Processes:                                                                  |
    # |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    # |        ID   ID                                                   Usage      |
    # |=============================================================================|
    # |  No running processes found                                                 |
    # +-----------------------------------------------------------------------------+
    ```

!!! warning
    既に導入済みの手順は実施不要です。また、NVIDIA関係のセットアップ手順はあくまで参考程度としてください。詳細はNVIDIA公式の手順をご確認ください。

## AWSIMの起動確認

以下のコマンドでBuildして起動してください。

```bash
cd aichallenge-racingkart
make simulator
```

下記のようにシミュレータが現れたら成功です。
![AWSIM-Autoware](./images/awsim.png)

Autowareも起動してみましょう。

```bash
cd aichallenge-racingkart
make autoware-build # 一度もbuildしてない方のみでOK
make autoware-simulator
```

以下のような画面が現れたら成功です。

![AWSIM-Autoware](./images/awsim-and-autoware.png)

確認が終わったら、以下のコマンドを実行します。

```bash
make down
```

## GPU未搭載環境でのヘッドレス実行

GPU未搭載の場合には、以下の手順でAWSIMをヘッドレスモードで実行する必要があります。この場合AWSIM画面は非表示ですが、RViz上で状況を確認できます。

1. `aichallenge-racingkart/aichallenge/simulator_scripts/dev.sh` 内で、`AWSIM.x86_64` の起動オプションに `-headless` を追加してください。
    - 注意：末尾に追加する場合は、直前の既存オプションの行末に「`\`」を忘れずにつけてください。
2. `aichallenge-racingkart/docker-compose.yml` から `- /dev/dri:/dev/dri` の記載を削除してください。

## Camera/LiDAR設定の切り替え { #camera-lidar }

- デフォルトでは、CameraとLiDARは無効状態です。End to End AI 部門参加者はCameraとLiDARを有効にする必要があります。
  - AI 部門参加者はNVIDIA GPU搭載パソコンを想定しています。そのため、 `gpu` に設定することを推奨します。
- `aichallenge-racingkart/aichallenge/simulator_scripts/dev.sh` 内で、`AWSIM.x86_64` の起動オプションの修正をしてください。
    - ローカル評価実行の場合には、 `eval.sh` を同様に編集してください。
    - 安全ゲートシナリオ実行の場合には、 `gate.sh` を同様に編集してください。

```bash
# Cameraの設定
## 無効 (デフォルト)
--camera off

## 有効 (CPU処理)
--camera cpu

## 有効 (GPU処理)
--camera gpu
```

```bash
# LiDARの設定
## 無効 (デフォルト)
--lidar off

## 有効 (CPU処理)
--lidar cpu

## 有効 (GPU処理)
--lidar gpu
```
