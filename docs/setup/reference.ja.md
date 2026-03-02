# 開発の参考

## 変更点の取り込み

大会環境の重大なアップデートがあった際には適宜アナウンスがあります。
参考までにこちらに記載しています。以下を実行してください。

### Dockerの更新

```bash
docker pull ghcr.io/automotiveaichallenge/autoware-universe:humble-latest
```

### Autowareの更新

```sh
cd aichallenge-racingkart # path to aichallenge
git pull origin/main
```

### AWSIMの更新

One DriveからSimPracticeFor2026内の `AWSIM.zip` をダウンロードし、`aichallenge-racingkart/aichallenge/simulator` に展開します。

[:material-launch: AWSIMの練習ファイルのダウンロード](https://tier4inc-my.sharepoint.com/:f:/g/personal/taiki_tanaka_tier4_jp/IgCivzVKr4HDSbS1BpXObYmGASNQ6uv7iVjKc6ysyBMernE){ .md-button .md-button--primary  target="_blank" }

※現在は大会期間外のため、練習用のファイルのみを提供しています。大会用のファイルは変更される可能性がありますのでご了承ください。

実行ファイルが`aichallenge-racingkart/aichallenge/simulator/AWSIM/AWSIM.x86_64`に存在していることを確認してください。

パーミッションを図のように変更します。

   ![パーミッション変更の様子](./images/awsim-permmision.png)

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

## Debug用に追加のTerminalを用意して開発したい場合 (参考)

`make dev`で起動した状態で、Autowareコンテナに追加のターミナルを接続できます。

`Alt+Ctrl+T`で新しいターミナルを開き、以下のコマンドで起動中のAutowareコンテナに入ります。

```bash
cd ~/aichallenge-racingkart
docker compose exec autoware bash
```

コンテナ内でROSトピックの確認やデバッグコマンドを実行できます。

```bash
# トピック一覧の確認
ros2 topic list

# 特定トピックの監視
ros2 topic echo /awsim/status
```

終了するには各ターミナル上でCTRL + Cを入力し、`make down`で全体を停止します。
![autoware](./images/autoware.png)
