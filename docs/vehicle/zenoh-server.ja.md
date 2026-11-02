# Zenoh 中継サーバー

遠隔 PC と車両 ECU の Zenoh bridge は、EC2 上の中継 router（`zenohd`）に mTLS で接続します。このページは、その中継サーバーを立てる手順です。遠隔 PC 側の手順は[遠隔操作](remote.ja.md)、ECU 側は[ECU の初期構築](ecu-setup.ja.md)を参照してください。

```text
遠隔 PC: joy_node → zenoh-bridge-ros2dds (-n /Ax) ─┐
                                                   ├─ mTLS → EC2: zenohd（号機ごとに別プロセス・別ポート）
ECU:     Autoware ↔ zenoh-bridge-ros2dds (-n /Ax) ─┘
```

router は号機ごとに別のポートで動かし、router 同士はつなぎません。遠隔 PC と ECU が同じ号機のポートにつながったときだけ、その2台の間でトピックが流れます。

## 1. EC2 インスタンスを立てる

- OS は Ubuntu 22.04（x86_64）にします。ROS 2 は要りません。router は軽いので、t3.micro 程度で足ります。
- security group で、号機ごとのポートを TCP で開けます。号機ごとのポートは、本体リポジトリの [`vehicle/vehicle_ports.sh`](https://github.com/AutomotiveAIChallenge/aichallenge-racingkart/blob/dev/vehicle/vehicle_ports.sh) で決まっています。
- EC2 に Elastic IP を割り当て、その IP を DNS 名 `zenoh.dev.aichallenge-board.jsae.or.jp` の A レコードに登録します。遠隔 PC と ECU はこの名前でつなぎ、server 証明書もこの名前で発行します。自動で付く公開 IP は EC2 を停止・起動すると変わるので、Elastic IP を使います。

## 2. 証明書を置く

mTLS の証明書は、server 用と client 用で別の CA（[minica](https://github.com/jsha/minica)）から発行します。client CA は号機の組ごとに分けられます。組ごとに別の client CA で client 証明書を発行し、その組の号機の遠隔 PC と ECU に配ります。

証明書は手元の端末で発行します。minica は Go で書かれているので、先に Go を入れておきます（Ubuntu では `golang-go` パッケージ）。`go install` で入れた minica は `$(go env GOPATH)/bin` に入ります。

```bash
go install github.com/jsha/minica@v1.1.0
export PATH="${PATH}:$(go env GOPATH)/bin"
mkdir -p ~/zenoh_tls/server
cd ~/zenoh_tls/server && minica --domains zenoh.dev.aichallenge-board.jsae.or.jp
```

server CA（`~/zenoh_tls/server/` の `minica.pem` と `minica-key.pem`）は最初に1回だけ作り、消さずに残します。作り直すと server CA が変わり、配った `tls.zip` が使えなくなります。client CA と client 証明書は、組ごとに `ca_dir` を変えて発行します。

```bash
ca_dir=client-xxxx   # client CA の組の名前。client- で始める
mkdir -p ~/zenoh_tls/"${ca_dir}"
cd ~/zenoh_tls/"${ca_dir}" && minica --domains aichallenge-zenoh-client
openssl x509 -in aichallenge-zenoh-client/cert.pem -noout -ext extendedKeyUsage   # TLS Web Client Authentication を含むこと
```

EC2 に置くのは、server 証明書と鍵、組ごとの client CA（`minica.pem`）だけです。CA の鍵（`minica-key.pem`）と client 証明書は置きません。手元の端末から、この3種類だけを同じ構成で EC2 の `~/zenoh_tls_upload` に送ります。

```bash
cd ~/zenoh_tls
server_name=zenoh.dev.aichallenge-board.jsae.or.jp
ec2=xxxx   # EC2 に ssh で入るときの宛先
rsync -a --relative "server/${server_name}/cert.pem" "server/${server_name}/key.pem" client-*/minica.pem "${ec2}:zenoh_tls_upload/"
```

EC2 内で `/etc/zenoh/tls/` の下に置きます。zenohd パッケージを更新・削除すると `/etc/zenohd` は消えるので、そこには置きません。router は root で動くので、鍵は root だけが読める 0600 にします。

```bash
server_name=zenoh.dev.aichallenge-board.jsae.or.jp
src=~/zenoh_tls_upload
for ca in "${src}"/client-*/minica.pem; do
  ca_dir=$(basename "$(dirname "${ca}")")
  sudo install -d -m 0755 "/etc/zenoh/tls/${ca_dir}"
  sudo install -m 0644 "${ca}" "/etc/zenoh/tls/${ca_dir}/minica.pem"
done
sudo install -d -m 0755 "/etc/zenoh/tls/server/${server_name}"
sudo install -m 0644 "${src}/server/${server_name}/cert.pem" "/etc/zenoh/tls/server/${server_name}/cert.pem"
sudo install -m 0600 "${src}/server/${server_name}/key.pem" "/etc/zenoh/tls/server/${server_name}/key.pem"
rm -r "${src}"
```

遠隔 PC と ECU には、組ごとに `tls.zip` を配ります。zip の中は、`tls/server/minica.pem`（`~/zenoh_tls/server/minica.pem`）と、`tls/client/cert.pem`・`tls/client/key.pem`（`~/zenoh_tls/<組>/aichallenge-zenoh-client/` の2つ）にします。置き方は[遠隔操作](remote.ja.md)の 1-6 と[ECU の初期構築](ecu-setup.ja.md)の 4-4 にあります。

## 3. 依存を入れる

EC2 内で、Eclipse Zenoh の apt リポジトリから `zenohd` を、版を指定して入れます。`apt upgrade` で版が変わらないよう hold します。パッケージに付いてくる `zenohd.service` は使わないので、無効にします。

```bash
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://download.eclipse.org/zenoh/debian-repo/zenoh-public-key |
  sudo gpg --dearmor --yes -o /etc/apt/keyrings/zenoh-public-key.gpg
echo 'deb [signed-by=/etc/apt/keyrings/zenoh-public-key.gpg] https://download.eclipse.org/zenoh/debian-repo/ /' |
  sudo tee /etc/apt/sources.list.d/zenoh.list >/dev/null
sudo apt-get update
apt-cache madison zenohd   # 入れられる版の一覧
zenohd_version=x.y.z       # 上の一覧から選んだ版
sudo apt-get install -y "zenohd=${zenohd_version}"
sudo apt-mark hold zenohd
sudo systemctl disable --now zenohd
```

## 4. systemd service を用意する

号機ごとに、router の設定と systemd service を作ります。EC2 内で、号機ごとに `vehicle_id`、`port`、`ca_dir` を変えて、次の2つを実行します。

```bash
vehicle_id=A2
port=7448            # この号機のポート（vehicle/vehicle_ports.sh）
ca_dir=client-xxxx   # この号機の組の client CA（/etc/zenoh/tls/ の下のディレクトリ名）
server_name=zenoh.dev.aichallenge-board.jsae.or.jp
sudo install -d -m 0755 /etc/zenoh/routers
sudo tee "/etc/zenoh/routers/router-${vehicle_id,,}.json5" >/dev/null <<EOF
{
  "mode": "router",
  "scouting": {
    "multicast": { "enabled": false },
    "gossip": { "enabled": false }
  },
  "listen": {
    "endpoints": ["tls/0.0.0.0:${port}"]
  },
  "connect": {
    "endpoints": []
  },
  "transport": {
    "unicast": {
      "compression": { "enabled": true }
    },
    "multicast": {
      "compression": { "enabled": true }
    },
    "link": {
      "tls": {
        "root_ca_certificate": "/etc/zenoh/tls/${ca_dir}/minica.pem",
        "enable_mtls": true,
        "listen_private_key": "/etc/zenoh/tls/server/${server_name}/key.pem",
        "listen_certificate": "/etc/zenoh/tls/server/${server_name}/cert.pem"
      }
    }
  }
}
EOF
```

- `scouting` を無効にし、`connect` を空にして、router 同士をつながないようにします。
- `root_ca_certificate` には、その号機の組の client CA を指定します。bridge の client 証明書はこれで検証されます。
- `enable_mtls` で、client 証明書のない接続を断ります。

```bash
sudo tee "/etc/systemd/system/zenoh-router-${vehicle_id,,}.service" >/dev/null <<EOF
[Unit]
Description=zenoh router ${vehicle_id}
After=network-online.target
Wants=network-online.target

[Service]
User=root
ExecStart=/usr/bin/zenohd -c /etc/zenoh/routers/router-${vehicle_id,,}.json5
Restart=always
RestartSec=2s
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now "zenoh-router-${vehicle_id,,}"
systemctl status "zenoh-router-${vehicle_id,,}" --no-pager   # active (running)
```

`journalctl -u zenoh-router-a2` に TLS や設定の読み込みのエラーが出ていないことを確かめます。遠隔 PC と ECU からつながるかは、[遠隔操作](remote.ja.md)の第2部で確かめます。
