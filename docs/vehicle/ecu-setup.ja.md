# ECU の初期構築

実車両に載せる ECU を、Ubuntu のインストールから始めて `./setup_check.sh --phase preflight` が通る状態にするまでの手順です。

この作業は運営が実施します。参加チームが構築済みの ECU で実車両を走らせる手順は[実車両の起動](run.ja.md)を参照してください。

## 第1部 OS とユーザー

### 1-1. 用意するもの

- MiniPC
- Ubuntu インストール用の USB メモリ
- Docker イメージインストール用の SSD（容量が大きいので SSD 推奨）
- インターネット接続のある有線 LAN

### 1-2. USB メディアを作成

[Ubuntu 22.04 の iso ファイル](https://releases.ubuntu.com/22.04/)を、[公式チュートリアル](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#1-overview)を参考に USB メモリへ書き込みます。

LAN ケーブルを挿してインターネット接続を確保した上で、以下の選択で USB インストールを進めます。

| 項目 | 設定値 |
| --- | --- |
| 言語 | English（インストール後に日本語へ切り替える） |
| キーボードレイアウト | Japanese / Japanese |
| インストール種別 | Normal Installation ＋ Download updates while installing Ubuntu |
| ディスク | Erase disk and install Ubuntu |
| タイムゾーン | Tokyo |
| Your computer's name | 号機ごとの設定値表の ECU ホスト名（例 `ECU-RK-01`） |
| Your name / username | 管理ユーザー（別途配布） |

インストール後、`Settings > Region & Language` で表示言語を日本語に変更します。

### 1-3. 管理ユーザーの初期設定

以降のコマンドはすべて管理ユーザーで実行します。参加者アカウントは別途追加します。

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

## 第2部 リポジトリと Docker 環境

### 2-1. リポジトリの取得と環境構築

`curl` を入れてから、セットアップスクリプトを実行します。リポジトリの clone から Docker のインストール、Autoware イメージの取得までを一括で行います。

```bash
sudo apt update
sudo apt install -y curl
curl -fsSL "https://raw.githubusercontent.com/AutomotiveAIChallenge/aichallenge-racingkart/main/setup.bash" | bash
```

| プロンプト | ECU での回答 | 理由 |
| --- | --- | --- |
| `Download AWSIM.zip and extract` | n | ECU では AWSIM を起動しないため（約数 GB の節約） |
| `Run make dev (ROS_DOMAIN_ID from .env)` | n | AWSIM を使うシミュレータ起動なので不要 |

VCU と GNSS のシリアルデバイスを開くために、手動で以下を実行します。

```bash
sudo usermod -aG dialout "$USER"
```

反映させるために再ログインし、以下のコマンドで反映されているか確認します。

```bash
groups            # docker と dialout が含まれること
```

### 2-2. racing_kart_interface イメージのインストール

共有された `racing_kart_interface_latest-experiment.tar.gz` と `.sha256` を、作業用 PC で外部 SSD にコピーしておきます。

外部 SSD を ECU に挿し、デバイス名を確認してから固定パスへマウントします。

```bash
lsblk -f                                       # 外部 SSD のデバイス名（例: sdb1）を確認
sudo mkdir -p /mnt/racing_kart_image_transfer
sudo mount /dev/sdX1 /mnt/racing_kart_image_transfer
```

`/dev/sdX1` は `lsblk -f` で確認した実際のデバイス名に置き換えてください。

tar ファイルが壊れていないことを確認します。

```bash
cd /mnt/racing_kart_image_transfer
sha256sum -c racing_kart_interface_latest-experiment.tar.gz.sha256
```

`racing_kart_interface_latest-experiment.tar.gz: OK` と表示されれば正常です。

イメージを load します。`docker load` は gzip 圧縮のまま読めるので、展開は不要です。

```bash
docker load -i /mnt/racing_kart_image_transfer/racing_kart_interface_latest-experiment.tar.gz
```

参照するタグが入っていることを確認します。

```bash
docker image inspect ghcr.io/tier4/racing_kart_interface:latest-experiment --format '{{.RepoTags}} {{.Id}} {{.Created}}'
```

`ghcr.io/tier4/racing_kart_interface:latest-experiment` が表示されれば OK です。

SSD をアンマウントします。

```bash
cd ~
sudo umount /mnt/racing_kart_image_transfer
```

## 第3部 udev ルールの設定

VCU と GNSS は `ttyUSB*` / `ttyACM*` の番号が挿抜のたびに変わるので、固定名の udev ルールを作ります。

### 3-1. VCU の udev ルール

```bash
sudo vim /etc/udev/rules.d/89-vcu.rules
```

```text
KERNEL=="ttyUSB[0-9]*", ENV{ID_MODEL}=="CP2102N_USB_to_UART_Bridge_Controller", SYMLINK+="vcu/usb", MODE="0666"
```

### 3-2. GNSS の udev ルール

```bash
sudo vim /etc/udev/rules.d/90-gnss.rules
```

```text
SUBSYSTEM=="tty", KERNEL=="ttyACM*", ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01a9", SYMLINK+="gnss/usb", MODE="0660", GROUP="dialout"
```

### 3-3. ルールの反映と確認

作成した2つのルールを反映します。

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

VCU と GNSS を接続して、symlink と所有グループを確認します。

```bash
ls -l /dev/vcu/usb /dev/gnss/usb
ls -lL /dev/gnss/usb   # dialout グループになっていること
```

### 3-4. CAN ツールの導入

`setup_check.sh` の `candump` チェック用に、CAN のツールも入れておきます。

```bash
sudo apt install -y can-utils
```

## 第4部 ネットワーク

ECU はネットワーク接続に Wi-Fi を使わず、有線接続のみで運用します。内蔵 Wi-Fi を有効なまま残すと、意図せず何らかのネットワークへ接続し、有線接続とデフォルトルートを争うことがあります。使わない機能なので先に無効化します。

### 4-1. 内蔵 Wi-Fi の無効化

MAC アドレスは筐体ごとに異なるので、対象 ECU 上で実測します。

```bash
ip link show                                  # wlp* / wlan* の内蔵 IF 名を特定
cat /sys/class/net/<内蔵IF名>/address          # 例: c0:4b:24:c1:03:de
```

udev でリンクを down させます。

```bash
sudo vim /etc/udev/rules.d/10-disable-internal-wifi.rules
```

```text
SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="c0:4b:24:c1:03:de", RUN+="/usr/bin/ip link set %k down"
```

udev で down させても NetworkManager が再度上げてしまうため、NetworkManager 側でも管理対象から外します。

```bash
sudo vim /etc/NetworkManager/conf.d/99-unmanage-internal-wifi.conf
```

```ini
[keyfile]
unmanaged-devices=mac:c0:4b:24:c1:03:de
```

上記の MAC は例です。実測値に置き換えてください。反映して確認します。

```bash
sudo systemctl restart NetworkManager
nmcli device status            # 内蔵 Wi-Fi が unmanaged / down になっていること
```

### 4-2. ファイアウォールの無効化

ファイアウォールを無効化します。

```bash
sudo ufw disable
```

### 4-3. SSH の有効化

SSH で接続できるようにしておきます。

```bash
sudo apt install -y openssh-server
systemctl is-enabled ssh      # enabled であること
```

## 第5部 ホストの ROS 2 環境

ホストからも `ros2` コマンドが使えるように、ROS 2 のセットアップもしておきます。

### 5-1. ROS 2 Humble とビルドツール

[公式手順](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)に従って `ros-humble-desktop` を入れます。

### 5-2. CycloneDDS（`/opt/autoware/cyclonedds.xml`）

ホスト側の設定ファイルはリポジトリ同梱のものをコピーして使います（コンテナ側は `docker-compose.yml` が `vehicle/cyclonedds.xml` をマウントするので別物です）。

```bash
sudo apt install -y ros-humble-rmw-cyclonedds-cpp
sudo mkdir -p /opt/autoware
sudo cp ~/aichallenge-racingkart/vehicle/cyclonedds.xml /opt/autoware/cyclonedds.xml
grep -i NetworkInterface /opt/autoware/cyclonedds.xml    # name="lo" があること
```

### 5-3. `~/.bashrc` に入れるもの

`~/.bashrc` に追記します。ROS 2 の環境変数に加えて、Docker コンテナ内で起動した GUI アプリ（RViz など）をホストの画面に描画するための設定もここでまとめて入れます。

```bash
export PATH=$HOME/.local/bin:$PATH
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///opt/autoware/cyclonedds.xml
export XAUTHORITY=$HOME/.Xauthority
xhost +SI:localuser:root >/dev/null 2>&1
```

## 第6部 動作確認

VCU・GNSS・PCAN-USB をすべて USB に接続した状態で実行します。繋がっていないとハードウェアのチェックが FAIL になります。

ここまでの手順が終わったら、FAIL が無いことを確認します。

```bash
cd ~/aichallenge-racingkart/vehicle
./setup_check.sh --phase preflight
```

ここまでで ECU の構築は完了です。実車両を走らせる手順は[実車両の起動](run.ja.md)を参照してください。
