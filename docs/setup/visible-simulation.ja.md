# 描画ありAWSIMのダウンロード (参考)

!!! warning "🚧 準備中 / Under Construction"
    シミュレータは大会開始と同時に公開されます。

デフォルトで描画なしのAWSIMを配布しておりますが、描画ありを希望される方の環境構築方法も記載しております。GPUを使用する環境構築では詰まって進まなくなる事例が多々ありましたので、[推奨環境](./requirements.ja.md)を満たすのスペックのPCが用意できない方や初めてのご参加の方はあくまでも参考程度としてください。

## NVIDIAドライバのインストール

```bash
# リポジトリの追加
sudo add-apt-repository ppa:graphics-drivers/ppa

# パッケージリストの更新
sudo apt update

# インストール
sudo ubuntu-drivers install

# 再起動
reboot

# 再起動の後、インストールできていることを確認
nvidia-smi
```

![nvidia-smi](./images/nvidia-smi.png)

## NVIDIA Container Toolkit

[NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)を参考にインストールを行います。

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

#インストールできているかをテスト
sudo docker run --rm --runtime=nvidia --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi

#最後のコマンドで以下のように出力されれば成功です。
#（下記はNVIDIAウェブサイトからの引用です）
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

## Vulkunのインストール

```bash
sudo apt update
sudo apt install -y libvulkan1
```

## AWSIMのダウンロード（シミュレータの配布は大会開始時になります）

1. Google Drive から最新の `AWSIM_GPU_**.zip` をダウンロードし、`aichallenge-2025/aichallenge/simulator` に展開します。

2. 実行ファイルが`aichallenge-2025/aichallenge/simulator/AWSIM/AWSIM.x86_64`に存在していることを確認してください。

3. パーミッションを図のように変更します。

   ![パーミッション変更の様子](./images/awsim-permmision.png)

## AWSIMの起動確認

描画ありのAWSIMを使用する場合は、以下のコマンドでコンテナを起動してください。

```bash
cd aichallenge-2025
./docker_build.sh dev
./docker_run.sh dev gpu
```

コンテナを起動したターミナル(コンテナ内)で以下を実行します。

```bash
cd /aichallenge
./build_autoware.bash
```

Autowareのビルド後、run_simulator.bashを変更します。`AISIM_GPU_**`には先程展開したディレクトリを指定してください。

```bash
#!/bin/bash

# shellcheck disable=SC1091
source /aichallenge/workspace/install/setup.bash
sudo ip link set multicast on lo
/aichallenge/simulator/AWSIM_GPU_**/AWSIM.x86_64
```

run_evaluetion.bashに対しても同様に次の変更を加えます。

```bash
# AWSIM_DIRECTORY=/aichallenge/simulator/AWSIM
AWSIM_DIRECTORY=/aichallenge/simulator/AWSIM_GPU_**
```

以下のコマンドを実行します。

```bash
./run_evaluation.bash
```

以下のような画面が現れたら成功です。

![AWSIM-Autoware](./images/awsim-and-autoware.png)

以上で環境構築は終了となります！

## Next Step: 開発をしてみる

[はじめ方](../getting-started.ja.md)から開発をしてみましょう！
