# GPUの活用

!!! warning
    GPUによるアクセラレーションありを希望される方の環境構築方法も記載しております。GPUを使用する環境構築では詰まって進まなくなる事例が多々ありましたので、[推奨環境](./requirements.ja.md)を満たすのスペックのPCが用意できない方や初めてのご参加の方はあくまでも参考程度としてください。

??? info "導線の案内"
    標準のセットアップ導線は [環境構築の流れ](./introduction.ja.md) を参照してください。
    このページは、GPU利用時に必要な追加手順（ドライバ/Toolkit/検証）をまとめた詳細参照用です。

???+ note "GPUオプションで追加すること"

    GPU利用時は、追加で下記を行います。

    - NVIDIAドライバ導入（原則再起動推奨）
    - NVIDIA Container Toolkit導入
    - GPU対応コンテナ実行テスト（`nvidia-smi`）
    - Vulkan導入とシミュレータ起動確認

??? note "GPUオプション: NVIDIAドライバのインストール手順"
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

??? note "GPUオプション: NVIDIA Container Toolkit のインストール手順"
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

??? note "Vulkanのインストール手順"
    ```bash
    sudo apt update
    sudo apt install -y libvulkan1

    ```

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

以上で環境構築は終了となります！

## [Next Step: 大会用のリポジトリのビルド・実行](./build-docker.ja.md)
