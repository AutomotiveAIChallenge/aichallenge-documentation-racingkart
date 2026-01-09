# 大会用リポジトリのビルド・実行

大会用リポジトリでは、実際の動作環境はすべてDocker内で完結して提供されています。リポジトリの利用は以下の流れで行います。

1. 大会環境のDockerイメージのビルド
2. Dockerコンテナ上でのAutowareのビルド
3. Dockerコンテナ上でのAutowareとシミュレータの同時起動

## Dockerコンテナ上でのAutowareのビルド

以下を実行してDockerコンテナを立ち上げます。

```bash
cd ~/aichallenge-2025
./docker_run.sh dev cpu
```

特に何も変わっていないように見えますが、上記のコマンドを実行すると環境がDockerコンテナ内部に移行します。今の環境がDockerコンテナ内かどうかは以下のコマンドで何も表示されていないかを確認するのがわかりやすいです。

```bash
ls ~
```

Dockerコンテナ内で以下を実行してAutowareをビルドします。

```bash
cd /aichallenge
./build_autoware.bash
```

## Dockerコンテナ上でのAutowareとSimulatorの実行

Autowareのビルド後、以下のコマンドを実行します。

```bash
./run_evaluation.bash
```

下記の様な画面が表示されたら起動完了です。終了するにはターミナル上でCTRL + Cを入力します。
![autoware](./images/autoware.png)

## [Next Step: 開発をしてみる](../development/workspace-usage.ja.md)

以上で環境構築は終了です！次は実際に開発を行ってみましょう。
