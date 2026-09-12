# Initial ECU Setup

This page describes how to take the ECU that is mounted on the real vehicle from a fresh Ubuntu installation to the point where `./setup_check.sh --phase preflight` passes.

This work is carried out by the organizers. For the procedure participating teams follow to run the real vehicle on an already-configured ECU, see [Starting the Real Vehicle](run.md).

## Part 1: OS and Users

### 1-1. What you need

- MiniPC
- USB stick for installing Ubuntu
- SSD for installing the Docker images (an SSD is recommended because the images are large)
- Wired LAN with an Internet connection

### 1-2. Create the USB installation media

Write the [Ubuntu 22.04 ISO file](https://releases.ubuntu.com/22.04/) to a USB stick, following the [official tutorial](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#1-overview).

Plug in a LAN cable so the machine has Internet access, then proceed with the USB installation using the following choices.

| Item | Setting |
| --- | --- |
| Language | English (switch to Japanese after installation) |
| Keyboard layout | Japanese / Japanese |
| Installation type | Normal Installation + Download updates while installing Ubuntu |
| Disk | Erase disk and install Ubuntu |
| Time zone | Tokyo |
| Your computer's name | The ECU host name from the per-vehicle settings table (e.g. `ECU-RK-01`) |
| Your name / username | Administrator user (distributed separately) |

After installation, change the display language to Japanese in `Settings > Region & Language`.

### 1-3. Initial setup of the administrator user

Run all of the following commands as the administrator user. Participant accounts are added separately.

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

## Part 2: Repository and Docker Environment

### 2-1. Get the repository and set up the environment

Install `curl`, then run the setup script. It clones the repository, installs Docker, and pulls the Autoware image in one go.

```bash
sudo apt update
sudo apt install -y curl
curl -fsSL "https://raw.githubusercontent.com/AutomotiveAIChallenge/aichallenge-racingkart/main/setup.bash" | bash
```

The script asks for confirmation before each step. Answer `n` to the following two prompts and `y` to all others.

| Prompt | Answer on the ECU | Reason |
| --- | --- | --- |
| `Download AWSIM.zip and extract` | n | AWSIM is not run on the ECU (saves several GB) |
| `Run make dev (ROS_DOMAIN_ID from .env)` | n | Not needed: this launches the simulator, which uses AWSIM |

The prompts are in `[y/N]` format, and **pressing Enter without typing anything counts as `n`**. For steps you want to run, explicitly type `y`.

To be able to open the VCU and GNSS serial devices, run the following manually.

```bash
sudo usermod -aG dialout "$USER"
```

Log in again for this to take effect, then confirm it with the following command.

```bash
groups            # docker と dialout が含まれること
```

(The output must include `docker` and `dialout`.)

### 2-2. Install the racing_kart_interface image

On a work PC, copy the shared `racing_kart_interface_latest-experiment.tar.gz` and its `.sha256` file to an external SSD.

Plug the external SSD into the ECU, check its device name, and mount it at a fixed path.

```bash
lsblk -f                                       # 外部 SSD のデバイス名（例: sdb1）を確認
sudo mkdir -p /mnt/racing_kart_image_transfer
sudo mount /dev/sdX1 /mnt/racing_kart_image_transfer
```

(The `lsblk -f` comment means: find the external SSD's device name, e.g. `sdb1`.) Replace `/dev/sdX1` with the actual device name you found with `lsblk -f`.

Check that the tar file is not corrupted.

```bash
cd /mnt/racing_kart_image_transfer
sha256sum -c racing_kart_interface_latest-experiment.tar.gz.sha256
```

If `racing_kart_interface_latest-experiment.tar.gz: OK` is shown, the file is intact.

Load the image. `docker load` can read the gzip-compressed file directly, so there is no need to extract it.

```bash
docker load -i /mnt/racing_kart_image_transfer/racing_kart_interface_latest-experiment.tar.gz
```

Confirm that the referenced tag is present.

```bash
docker image inspect ghcr.io/tier4/racing_kart_interface:latest-experiment --format '{{.RepoTags}} {{.Id}} {{.Created}}'
```

If `ghcr.io/tier4/racing_kart_interface:latest-experiment` is shown, you are done.

Unmount the SSD.

```bash
cd ~
sudo umount /mnt/racing_kart_image_transfer
```

## Part 3: udev Rules

The `ttyUSB*` / `ttyACM*` numbers of the VCU and GNSS change every time they are unplugged and replugged, so create udev rules that give them fixed names.

### 3-1. udev rule for the VCU

```bash
sudo vim /etc/udev/rules.d/89-vcu.rules
```

```text
KERNEL=="ttyUSB[0-9]*", ENV{ID_MODEL}=="CP2102N_USB_to_UART_Bridge_Controller", SYMLINK+="vcu/usb", MODE="0666"
```

### 3-2. udev rule for the GNSS

```bash
sudo vim /etc/udev/rules.d/90-gnss.rules
```

```text
SUBSYSTEM=="tty", KERNEL=="ttyACM*", ATTRS{idVendor}=="1546", ATTRS{idProduct}=="01a9", SYMLINK+="gnss/usb", MODE="0660", GROUP="dialout"
```

### 3-3. Apply and verify the rules

Apply the two rules you created.

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Connect the VCU and GNSS, then check the symlinks and the owning group.

```bash
ls -l /dev/vcu/usb /dev/gnss/usb
ls -lL /dev/gnss/usb   # dialout グループになっていること
```

(`/dev/gnss/usb` must belong to the `dialout` group.)

### 3-4. Install the CAN tools

Also install the CAN tools, which the `candump` check in `setup_check.sh` needs.

```bash
sudo apt install -y can-utils
```

## Part 4: Network

The ECU does not use Wi-Fi for networking; it is operated over a wired connection only. If the built-in Wi-Fi is left enabled, it may connect to some network unintentionally and compete with the wired connection for the default route. Since it is not used, disable it first.

### 4-1. Disable the built-in Wi-Fi

The MAC address differs for every unit, so read it on the target ECU itself.

```bash
ip link show                                  # wlp* / wlan* の内蔵 IF 名を特定
cat /sys/class/net/<内蔵IF名>/address          # 例: c0:4b:24:c1:03:de
```

(Identify the built-in interface name, `wlp*` / `wlan*`, then read its address, e.g. `c0:4b:24:c1:03:de`. Replace `<内蔵IF名>` with that interface name.)

Use udev to bring the link down.

```bash
sudo vim /etc/udev/rules.d/10-disable-internal-wifi.rules
```

```text
SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="c0:4b:24:c1:03:de", RUN+="/usr/bin/ip link set %k down"
```

Even after udev brings it down, NetworkManager will bring it up again, so also exclude it from NetworkManager's managed devices.

```bash
sudo vim /etc/NetworkManager/conf.d/99-unmanage-internal-wifi.conf
```

```ini
[keyfile]
unmanaged-devices=mac:c0:4b:24:c1:03:de
```

The MAC address above is an example; replace it with the value you measured. Apply and verify:

```bash
sudo systemctl restart NetworkManager
nmcli device status            # 内蔵 Wi-Fi が unmanaged / down になっていること
```

(The built-in Wi-Fi must show as `unmanaged` / down.)

### 4-2. Disable the firewall

Disable the firewall.

```bash
sudo ufw disable
```

### 4-3. Enable SSH

Make the ECU reachable over SSH.

```bash
sudo apt install -y openssh-server
systemctl is-enabled ssh      # enabled であること
```

(The output must be `enabled`.)

### 4-4. Place the TLS certificates

The vehicle ECU uses two kinds of TLS certificates. Neither is tracked in git, so place the distributed files on the ECU.

| Purpose | Location | Files |
| --- | --- | --- |
| zenoh (remote operation and remote visualization) | `~/aichallenge-racingkart/remote/tls/` | `server/minica.pem`, `client/cert.pem`, `client/key.pem` |
| V2X position sharing (MQTT broker) | `/etc/v2x/tls/` | `ca.crt`, `kart.crt`, `kart.key` |

#### For zenoh (`remote/tls/`)

```bash
cd ~/aichallenge-racingkart
sudo apt install -y unzip
unzip -o ~/Downloads/tls.zip -d remote/    # tls.zip の保存先は環境に合わせてください
chmod 600 remote/tls/client/key.pem
```

(Adjust the location of `tls.zip` to wherever you saved it.)

After extracting, check that the layout is as follows. If it differs, rearrange the files so that `remote/tls/` has this layout.

```bash
ls remote/tls          # client  server
ls remote/tls/client   # cert.pem  key.pem(600)
ls remote/tls/server   # minica.pem
```

The same procedure on the remote PC side is in step 1-6 of [Remote Operation](remote.md). The certificate contents are the same as on the vehicle side.

#### For V2X (`/etc/v2x/tls/`)

Place the distributed `ca.crt` / `kart.crt` / `kart.key`, owned by root.

```bash
cd ~/v2x-certs                             # 配布された証明書を展開したディレクトリに合わせてください
sudo mkdir -p /etc/v2x/tls
sudo cp ca.crt kart.crt kart.key /etc/v2x/tls/
sudo chown -R root:root /etc/v2x/tls
sudo chmod 700 /etc/v2x/tls
sudo chmod 600 /etc/v2x/tls/kart.key
sudo chmod 644 /etc/v2x/tls/ca.crt /etc/v2x/tls/kart.crt
```

(Change `~/v2x-certs` to the directory where you extracted the distributed certificates.)

Once placed, check the CN and the validity period.

```bash
sudo openssl x509 -in /etc/v2x/tls/kart.crt -noout -subject -dates
# subject=CN = d1   ← .env の V2X_VEHICLE_ID と一致すること
# notAfter=...      ← 走行日より先であること
sudo openssl verify -CAfile /etc/v2x/tls/ca.crt /etc/v2x/tls/kart.crt
# /etc/v2x/tls/kart.crt: OK
```

(The CN must match `V2X_VEHICLE_ID` in `.env`, and `notAfter` must be later than the day you drive.)

### 4-5. Collect logs from the LTE router

If you use a router with syslog forwarding, this setup lets you use the router's logs when the connection becomes unstable.

#### Give the ECU a static IP

The syslog forwarding destination is specified by IP address, so if the ECU stays on DHCP, forwarding stops as soon as its IP changes. Fix the IP to match the router's settings.

```bash
sudo nmcli con mod "Wired connection 1" \
    ipv4.method manual \
    ipv4.addresses 192.168.254.2/24 \
    ipv4.gateway 192.168.254.254 \
    ipv4.dns 192.168.254.254
sudo nmcli con up "Wired connection 1"
```

#### Receive syslog on the ECU

UDP reception is disabled in Ubuntu's rsyslog, so add a reception configuration.

```bash
sudo vim /etc/rsyslog.d/09-as250.conf
```

```text
module(load="imudp")
input(type="imudp" port="514")

# 受信側（ECU）の時刻とルータ申告の時刻を両方残す。
# ルータの NTP がずれていても ECU の時計で追えるようにするため。
template(name="AS250Format" type="string"
  string="%timegenerated:::date-rfc3339% | dev:%timereported:::date-rfc3339% | %fromhost-ip% | %syslogtag%%msg%\n")

if ($fromhost-ip == "192.168.254.254") then {
    action(type="omfile" file="/var/log/as250.log" template="AS250Format"
           fileCreateMode="0640" fileOwner="syslog" fileGroup="adm")
    stop
}
```

(The comments in the configuration say: keep both the receive time on the ECU and the time reported by the router, so that events can still be followed on the ECU's clock even if the router's NTP is off.)

Only lines whose sender is the router are routed to `/var/log/as250.log`, and `stop` keeps them from being mixed into the ECU's own syslog.

Also set up rotation so that the log does not grow without bound.

```bash
sudo vim /etc/logrotate.d/as250
```

```text
/var/log/as250.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0640 syslog adm
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
```

Apply the configuration and confirm rsyslog is listening, then add the firewall allowance and a link for viewing the log from your home directory.

```bash
sudo rsyslogd -N1 -f /etc/rsyslog.conf      # 構文チェック
sudo systemctl restart rsyslog
ss -lunp | grep :514                         # 514/udp を待ち受けていること
sudo ufw allow from 192.168.254.254 to any port 514 proto udp comment "AS-250/L syslog"
ln -sfn /var/log/as250.log ~/router.log      # rsyslog は syslog ユーザーで動くため $HOME には直接書かせない
```

(Comments: `rsyslogd -N1` is a syntax check; `ss` must show a listener on 514/udp; the symlink is used because rsyslog runs as the `syslog` user and is not allowed to write into `$HOME` directly.)

#### Verify reception

Confirm that log lines appear with the following command.

```bash
tail -f ~/router.log
```

## Part 5: ROS 2 Environment on the Host

Also set up ROS 2 so that the `ros2` command can be used on the host.

### 5-1. ROS 2 Humble

Add the apt repository, then install `ros-humble-desktop`. The steps are the same as the [official instructions](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

```bash
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

sudo apt install -y software-properties-common curl
sudo add-apt-repository -y universe
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

```bash
sudo apt update
sudo apt install -y ros-humble-desktop
```

The setting that makes the `ros2` command available when a shell starts is appended to `~/.bashrc` in 5-3, together with the other environment variables.

### 5-2. CycloneDDS (`/opt/autoware/cyclonedds.xml`)

On the host, copy and use the configuration file bundled with the repository (the containers use a separate copy: `docker-compose.yml` mounts `vehicle/cyclonedds.xml` into them).

```bash
sudo apt install -y ros-humble-rmw-cyclonedds-cpp
sudo mkdir -p /opt/autoware
sudo cp ~/aichallenge-racingkart/vehicle/cyclonedds.xml /opt/autoware/cyclonedds.xml
grep -i NetworkInterface /opt/autoware/cyclonedds.xml    # name="lo" があること
```

(The output must contain `name="lo"`.)

### 5-3. What goes into `~/.bashrc`

Append the following to `~/.bashrc`. In addition to the ROS 2 environment variables, this also includes the settings that let GUI applications started inside Docker containers (such as RViz) draw on the host's display.

```bash
export PATH=$HOME/.local/bin:$PATH
source /opt/ros/humble/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///opt/autoware/cyclonedds.xml
export XAUTHORITY=$HOME/.Xauthority
xhost +SI:localuser:root >/dev/null 2>&1
```

## Part 6: Verification

### 6-1. Set `VEHICLE_ID` in `.env`

`setup_check.sh` uses `VEHICLE_ID` from `.env` to check connectivity to the Zenoh server. Right after `setup.bash` creates it, `.env` contains the initial value `A0`, which is not a valid vehicle, so the check always FAILs. Open `~/aichallenge-racingkart/.env` at the repository root and change it to the value for the vehicle this ECU will be mounted on (see the per-vehicle settings table).

```diff
- VEHICLE_ID=A0
+ VEHICLE_ID=A2
```

The remaining items in `.env` (such as the NTRIP account) are set when driving. See [Starting the Real Vehicle](run.md).

### 6-2. Run `setup_check.sh`

Run it with the VCU, GNSS, and PCAN-USB all connected via USB. If any of them is not connected, the hardware checks FAIL.

Once all the steps above are done, confirm that there are no FAILs.

```bash
cd ~/aichallenge-racingkart/vehicle
./setup_check.sh --phase preflight
```

This completes the ECU setup. For how to run the real vehicle, see [Starting the Real Vehicle](run.md).
