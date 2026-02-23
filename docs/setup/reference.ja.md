# 開発の参考

## 変更点の取り込み

大会環境の重大なアップデートがあった際には適宜アナウンスがあります。
参考までにこちらに記載しています。以下を実行してください。

Dockerのupdate

```bash
docker pull ghcr.io/automotiveaichallenge/autoware-universe:humble-latest
```

Repositoryのupdate

```sh
cd aichallenge-racingkart # path to aichallenge
git pull origin/main
```

## 描画ありAWSIMの導入

AWSIMのシミュレーション画面を確認したい方は、[こちら](../setup/visible-simulation.ja.md)の手順に従って描画ありAWSIMの導入を行ってください。

## よく使う設定（環境変数）

環境変数は、コマンドの前に `NAME=value` を付けます（その1回だけ有効です）。

### GPUを使う/使わない（詰まったらまず `cpu`）

```bash
DEVICE=cpu make dev
DEVICE=gpu make eval
```

- `DEVICE=auto`（デフォルト）: `/dev/nvidia0` があれば GPU 扱い
- `DEVICE=gpu`: GPUを強制（Docker側のNVIDIA設定が必要）
- `DEVICE=cpu`: GPU設定を使わない（まず動かしたい時の保険）

### Domain ID（複数作業/衝突回避）

```bash
DOMAIN_ID=1 make autoware-simulator
DOMAIN_ID=2 make autoware-simulator
```

Domain ID は、同じマシンで複数セットを動かす時などに「衝突を避ける番号」です。迷ったら `1` のままで問題ありません。

## よくある詰まり（最短で戻る）

- **起動できない / `pull_policy: never` っぽいエラー**: まず `./docker_build.sh dev`
- **`.../install/setup.bash` が無い**: まず `make autoware-build`
- **とにかく一旦止めたい**: まず `make down`

## Debug用にTerminalを3つ用意して開発したい場合 (参考)

`Alt+Ctrl+T`で１つ目のターミナルを立ち上げてから、以下のコマンド`Ctrl+Shift+V`で貼り付けた後に`Enter`で実行します。

```bash
cd ~/aichallenge-racingkart
./docker_run.sh dev cpu
```

```bash
cd /aichallenge
bash run_simulator.bash
```

`Alt+Ctrl+T`で2つ目のターミナルを立ち上げてから、以下のコマンド`Ctrl+Shift+V`で貼り付けた後に`Enter`で実行します。

```bash
cd ~/aichallenge-racingkart
./docker_run.sh dev cpu
```

```bash
cd /aichallenge
bash run_autoware.bash
```

`Alt+Ctrl+T`で3つ目のターミナルを立ち上げてから、以下のコマンド`Ctrl+Shift+V`で貼り付けた後に`Enter`で実行します。

```bash
cd ~/aichallenge-racingkart
./docker_run.sh dev cpu
```

```bash
cd /aichallenge
ros2 topic pub --once /control/control_mode_request_topic std_msgs/msg/Bool '{data: true}' >/dev/null
```

下記の様な画面が表示されたら起動完了です。終了するには各ターミナル上でCTRL + Cを入力します。
![autoware](./images/autoware.png)
