# Autoware 基礎演習

## はじめに

!!! warning
    本講座で使用する環境（`autoware-practice`）は、AIチャレンジの大会環境（Docker + AWSIM）とは異なります。

本演習では Autoware の基礎について学んでいきます。
課題を達成するためのコードをゼロから開発しながら Autoware の仕組みを学べる演習形式となっています。
各演習ページにはメニューから移動してください。

## 環境構築

まず､ Autoware の動作に必要な ROS 2 をインストールします｡
[ROS 2 Documentation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html) の手順にしたがってEnvironment setupまでを完了させてください｡

つづけて､いくつかの開発支援ツールセットもインストールします｡

```bash
# Install rosdep
sudo apt install python3-rosdep
# Install vcstool
sudo apt install python3-vcstool
# Install colcon
sudo apt install python3-colcon-common-extensions
```

任意のディレクトリにて入門講座のリポジトリをクローンし、ビルドを行ってください。

```bash
git clone https://github.com/AutomotiveAIChallenge/autoware-practice.git
cd autoware-practice
vcs import src < autoware.repos
rosdep install -y --from-paths src --ignore-src --rosdistro humble
colcon build --symlink-install
```

ビルドが完了したら、以下のコマンドを実行してビルドされたパッケージを利用できるようにします。
また、今後演習の中でコマンドを実行する際は、事前にこちらのコマンドを実行しておいてください。

```bash
source install/setup.bash
```
