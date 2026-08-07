# AWSIM マルチプレイ 参加者ガイド

このガイドでは、AWSIMマルチプレイサーバーへの接続方法と、他の参加者との走行方法を説明します。

## Step 1 — WireGuardのインストール

```bash
sudo apt install wireguard
```

## Step 2 — VPNに接続する

運営からDMで設定ファイル(例: `alice.conf`)を受け取り好きなところに置きます。

```bash
# VPN接続
sudo wg-quick up /path/to/alice.conf
```

トンネルが立っているか確認:
```bash
sudo wg show

# 自分のpeerと、直近のhandshake時刻が表示されればOK
```

> このVPNは `10.0.0.0/24`(マルチプレイ用ネットワーク)のみをルーティングします。通常のインターネット接続には影響しません。

## Step 3 — AWSIMをクライアントモードで起動する

VPNが接続できたら、サーバーのVPNアドレスを指定してAWSIMを起動します。

```bash
# camera と lidarはオンにすることもできます
cd ~/aichallenge-racingkart/aichallenge/simulator/AWSIM
./AWSIM.x86_64 \
  --collisions off \
  --start-mode count \
  --start-count-seconds 0 \
  --wall-recovery off \
  --laps unlimited \
  --timeout 10000000.0 \
  --multiplay client \
  --multiplay-address 10.0.0.1 \
  --multiplay-port 7777 \
  --sound off \
  --camera off \
  --lidar off \
  --multiplay-name <あなたの名前>
```

- `<あなたの名前>` — 任意の表示名(ダッシュボードに表示されます)

AWSIMが接続すると、他の参加者のカートが参加するたびに画面上に表示されます。

## Step 4 — AWSIMをクライアントモードで起動する

以下のコマンドでAutowareとRvizを起動します。

```bash
make autoware-simulator 
```

## Step 5 — 終了時の切断

```bash
# VPNの切断
sudo wg-quick down ./alice.conf
```

参考: https://automotiveaichallenge.github.io/aichallenge-documentation-racingkart/development/multiplay.html#_4
