# 仮想環境のインストール

## 依存パッケージのインストール

まずは必要なライブラリをインストールします。

```bash
sudo apt update
sudo apt install -y python3-pip ca-certificates curl gnupg
```

## Dockerのインストール

[公式ドキュメント](https://docs.docker.com/engine/install/ubuntu/)通りに以下のコマンドでインストールします。

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

以下のコマンドで正常にインストールされているか確認してください。

```bash
sudo docker run hello-world
```

`Hello from Docker!`と表示されれば正常にインストール出来ています。

## rockerのインストール

rockerはDockerコンテナのGUIアプリを簡単に起動できるようにするツールです。

[公式README](https://github.com/osrf/rocker?tab=readme-ov-file#debians-recommended)ではaptからのインストールが推奨されていますが、手順と環境をシンプルにするためにここではpipからインストールします。

```bash
pip install rocker
```

デフォルト設定ではrockerの実行ファイルへのパスが通っていないので、以下のコマンドで`.bashrc`に追加しておきます。

```bash
echo export PATH='$HOME/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## Autoware環境のDockerイメージ取得

AIチャレンジで使用するautoware環境のDockerイメージを取得します。

Dockerイメージは10GB程度のサイズがあり、ダウンロードには時間が掛かるため有線LANでのダウンロードを推奨します。

```bash
docker pull ghcr.io/automotiveaichallenge/autoware-universe:humble-latest
```

以下のコマンドでダウンロードできているか確認します。

```bash
docker images
```

Dockerイメージがダウンロードできていれば以下のような出力が得られます。

```txt
REPOSITORY                                        TAG                       IMAGE ID       CREATED         SIZE
ghcr.io/automotiveaichallenge/autoware-universe   humble-latest             30c59f3fb415   13 days ago     8.84GB
```

## 大会環境のDockerイメージのビルド

再度`Alt+Ctrl+T`でターミナルを立ち上げて下さい。以下に従ってコマンドを`Ctrl+Shift+V`で貼り付け`Enter`で実行します。

まず大会用リポジトリに入ります。

```bash
cd ~/aichallenge-racingkart
```

Dockerイメージのビルドを行います。

```bash
./docker_build.sh dev
```

```bash
docker images
```

で以下のイメージが生成されていることを確認しましょう。

```txt
aichallenge-2025-dev   latest   df2e83a20349   33 minutes ago   8.9GB
```

## Next Step

2種類のAWSIMを提供しています。

初めての方は描画なしAWSIMへ、GPU搭載のPCをお持ちの方でよりリッチな開発環境をご用意されたい方は描画ありAWSIMのドキュメントにお進み下さい。

[描画なしAWSIMのダウンロード](./headless-simulation.ja.md)

[描画ありAWSIMのダウンロード](./visible-simulation.ja.md)
