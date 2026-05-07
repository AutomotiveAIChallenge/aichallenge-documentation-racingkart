# Autoware 入門講座

## はじめに

!!! warning
    本講座で使用する環境（`autoware-practice`）は、AIチャレンジの大会環境（Docker + AWSIM）とは異なります。

この講座では Autoware の基本的な開発方法について解説します。
講座は演習形式となっており、課題を達成するためのコードをゼロから開発しながら Autoware の仕組みを学べるようになっています。
各講座のページにはメニューから移動してください。

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
また、今後講座の中でコマンドを実行する際は、事前にこちらのコマンドを実行しておいてください。

```bash
source install/setup.bash
```
