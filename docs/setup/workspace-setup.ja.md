# ワークスペースのクローン

## 依存パッケージのインストール

`Alt+Ctrl+T`でターミナルを立ち上げてから、以下に従ってコマンドを`Ctrl+Shift+V`で貼り付け、`Enter`で実行します。
まずは必要なライブラリをインストールします。

```bash
sudo apt update
sudo apt install -y git
```

## 大会用リポジトリのクローン

ワークスペース用のリポジトリをクローンします。ここではホームディレクトリを指定していますが、お好きなディレクトリに配置していただいて構いません。

```bash
cd ~
git clone https://github.com/AutomotiveAIChallenge/aichallenge-2025.git
```

## [Next Step: 仮想環境のインストール](./docker.ja.md)
