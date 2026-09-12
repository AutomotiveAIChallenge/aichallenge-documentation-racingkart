# Remote Operation

Emergency stops and manual driving during a run are performed by remote operation, using a game controller connected to the remote PC.

For the vehicle-side startup procedure, see [Starting the Real Vehicle](run.md); for the initial setup of the ECU itself, see [Initial ECU Setup](ecu-setup.md).

The autonomous vehicle has a safety function that makes it stop in an emergency when communication between the remote PC and the vehicle is lost, or when the game controller is unplugged from the remote PC. Note, however, that the loss-detection threshold is 5 seconds, so the vehicle does not stop at the very moment the game controller is unplugged.

![Remote operation zenoh topology](./images/remote-topology.svg)

## Part 1: Common Setup

### 1-1. Install ROS 2 Humble

The remote PC is assumed to run Ubuntu 22.04 (Jammy). The steps are the same as the [official instructions](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

On the remote PC, `joy.bash` (`joy_node`) and the `ros2` command run on the host, so ROS 2 must be installed on the host. The setup script in 1-2 does not install ROS 2, so do this step separately.

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

Install `ros-humble-desktop`.

```bash
sudo apt update
sudo apt install -y ros-humble-desktop
```

Append the following to `~/.bashrc` so that the `ros2` command is available when a shell starts (the same file where the environment variables in 1-7 are added).

```bash
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
source ~/.bashrc
printenv ROS_DISTRO     # humble と表示されること
```

(The output must be `humble`.)

### 1-2. Get the repository and set up the environment

Install `curl`, then run the setup script. It clones the repository, installs Docker, and pulls the Autoware image in one go.

```bash
sudo apt update
sudo apt install -y curl
curl -fsSL "https://raw.githubusercontent.com/AutomotiveAIChallenge/aichallenge-racingkart/main/setup.bash" | bash
```

The `main` branch is cloned into `~/aichallenge-racingkart`.

The script asks for confirmation before each step. Answer `n` to the following two prompts and `y` to all others.

| Prompt | Answer on the remote PC | Reason |
| --- | --- | --- |
| `Download AWSIM.zip and extract` | n | AWSIM is not run on the remote PC (saves several GB) |
| `Run make dev (ROS_DOMAIN_ID from .env)` | n | Not needed: this launches the simulator, which uses AWSIM |

The prompts are in `[y/N]` format, and **pressing Enter without typing anything counts as `n`**. For steps you want to run, explicitly type `y`.

### 1-3. Re-check after setup

```bash
cd ~/aichallenge-racingkart
./setup.bash doctor
```

`doctor` only inspects the OS, tools, Docker, `.env`, and whether the images are present; it makes no changes to the system. Warnings about AWSIM are the result of answering n in 1-2 and can be ignored on the remote PC.

### 1-4. Zenoh bridge (installed on the host)

```bash
cd ~/aichallenge-racingkart
sudo dpkg -i vehicle/zenoh-bridge-ros2dds_1.5.0_amd64.deb
apt list --installed zenoh-bridge-ros2dds   # 1.5.0 であること
```

(The installed version must be 1.5.0.)

### 1-5. joy package for the game controller

```bash
sudo apt install -y ros-humble-joy
sudo usermod -aG input "$USER"
# 再ログインして反映する
```

(Log in again for the group change to take effect.)

### 1-6. Place the TLS certificates

Extract the distributed tls.zip into `remote/tls/` and set the permissions of the private key to 600.

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

### 1-7. CycloneDDS / RMW settings

On the host, copy and use the configuration file bundled with the repository (the containers use a separate copy: `docker-compose.yml` mounts `vehicle/cyclonedds.xml` into them).

```bash
sudo apt install -y ros-humble-rmw-cyclonedds-cpp
sudo mkdir -p /opt/autoware
sudo cp ~/aichallenge-racingkart/vehicle/cyclonedds.xml /opt/autoware/cyclonedds.xml
grep -i NetworkInterface /opt/autoware/cyclonedds.xml    # name="lo" があること
```

(The output must contain `name="lo"`.)

Append the following to `~/.bashrc`.

```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///opt/autoware/cyclonedds.xml
```

### 1-8. Set the vehicle number in `.env`

Open `.env` at the repository root and change the `VEHICLE_ID` line to match the target vehicle (wherever `Ax` appears below, replace it with the target vehicle, such as A3 or A6).

```diff
- VEHICLE_ID=A0
+ VEHICLE_ID=Ax
```

## Part 2: Checking Remote Operation on a Single Laptop

**Purpose**: Run both the "vehicle side" and the "remote side" on one PC, connect both as clients to the real EC2 server, and confirm that joy input reaches the vehicle side via EC2.

### 2-1. Procedure

Run the commands in separate terminals A to E. `make zenoh` in terminal A only starts a detached container and does not occupy the terminal, so the four terminals that must stay open are B to E. Terminals do not share a current directory, so start each terminal with the `cd` shown.

```bash
# 端末A: 車両側 zenoh bridge（domain1 → EC2）
cd ~/aichallenge-racingkart
make zenoh

# 端末B: 車両側の joy 受け手（domain1）。echo 自体が subscriber になり bridge が転送を開始
source /opt/ros/humble/setup.bash
ROS_DOMAIN_ID=1 ros2 topic echo /racing_kart/joy

# 端末C: 遠隔側 zenoh bridge（domain0 → EC2）
cd ~/aichallenge-racingkart/remote
ROS_DOMAIN_ID=0 ./connect_zenoh.bash Ax

# 端末D: 遠隔側で joy を流す（domain0）
source /opt/ros/humble/setup.bash
ROS_DOMAIN_ID=0 ros2 topic pub -r 10 /racing_kart/joy sensor_msgs/msg/Joy \
  '{header: {frame_id: "joy"}, axes: [0.1,0.5,0.0,0.0], buttons: [1,0,0,0]}'
```

Terminal roles (translation of the comments above):

- Terminal A (端末A): vehicle-side zenoh bridge (domain 1 → EC2).
- Terminal B (端末B): vehicle-side joy receiver (domain 1). The `echo` itself acts as the subscriber, which makes the bridge start forwarding.
- Terminal C (端末C): remote-side zenoh bridge (domain 0 → EC2).
- Terminal D (端末D): publish joy messages on the remote side (domain 0).

### 2-2. Pass/fail check

```bash
# 端末E
source /opt/ros/humble/setup.bash
ROS_DOMAIN_ID=1 ros2 topic hz /racing_kart/joy     # ~10Hz であること
```

(In terminal E, the rate must be about 10 Hz.)

### 2-3. Shutdown procedure

Terminals B, C, D, and E are foreground host processes, so `make down` does not stop them. Press Ctrl+C in each of those terminals first.

```bash
# 1) 端末B(echo) / 端末C(zenoh bridge) / 端末D(topic pub) / 端末E(hz) をそれぞれ Ctrl+C

# 2) 端末A で起動した zenoh コンテナを停止
cd ~/aichallenge-racingkart
make down

# 3) 残存していないことを確認
docker compose ps                  # 何も残っていないこと
pgrep -af zenoh-bridge-ros2dds     # 何も出ないこと
```

(Steps: 1) press Ctrl+C in terminal B (echo), C (zenoh bridge), D (topic pub), and E (hz); 2) stop the zenoh container started in terminal A; 3) confirm nothing is left: `docker compose ps` lists nothing and `pgrep` prints nothing.)

## Part 3: Real Vehicle and Remote PC Configuration

This is the production remote operation, connecting the real vehicle and the remote PC via EC2.
The remote PC connects to the vehicle side over zenoh via EC2, so **the remote PC must have an Internet connection**.

### 3-1. Connect the game controller

Connect the game controller (Logicool F310) to the remote PC with a USB cable.

### 3-2. Remote operation flow (remote PC side)

Run the commands in separate terminals A to C. `rviz.bash` in terminal C only starts a detached container and does not occupy the terminal, so the two terminals that must stay open are A and B.

On the remote PC, set `ROS_DOMAIN_ID` in `.env` to `0`. Terminals A and B run in the host's default domain, but RViz2 runs in a container and therefore reads the value from `.env`.

```diff
- ROS_DOMAIN_ID=1
+ ROS_DOMAIN_ID=0
```

Note that in the single-PC configuration of Part 2, the vehicle-side zenoh must be started in domain 1, so leave `.env` at `ROS_DOMAIN_ID=1` there.

```bash
# 端末A: joy_node（コントローラ入力 → /racing_kart/joy）
cd ~/aichallenge-racingkart/remote
ROS_DOMAIN_ID=0 ./joy.bash

# 端末B: 車両と zenoh 接続（EC2 へ client 接続 / TLS）
cd ~/aichallenge-racingkart/remote
ROS_DOMAIN_ID=0 ./connect_zenoh.bash Ax

# 端末C: RViz（遠隔可視化スタック）
cd ~/aichallenge-racingkart/remote
./rviz.bash
```

Terminal roles (translation of the comments above):

- Terminal A (端末A): `joy_node` (controller input → `/racing_kart/joy`).
- Terminal B (端末B): zenoh connection to the vehicle (client connection to EC2, over TLS).
- Terminal C (端末C): RViz (remote visualization stack).

`connect_zenoh.bash` resolves the TLS certificate paths in `zenoh-user.json5` relative to `remote/`, so it must be run with `remote/` as the current directory.

`rviz.bash` is a wrapper around `make rviz2` that starts rviz2 as a container (`./rviz.bash restart` reopens it and `./rviz.bash down` stops it).

### 3-3. Start the vehicle-side ECU

On the vehicle-side ECU, start driver / autoware / rosbag / zenoh separately with `make autoware-driver-zenoh-rosbag`. The vehicle-side procedure, including the `.env` settings and IMU bias adjustment, is in [Starting the Real Vehicle](run.md), and the initial setup of the ECU itself is in [Initial ECU Setup](ecu-setup.md).

### 3-4. Shutdown procedure

`joy.bash` (joy_node) in terminal A and `connect_zenoh.bash` (zenoh bridge) in terminal B are foreground processes on the host, and `make down` stops only Docker Compose services. Conversely, rviz2 is a detached container, so it keeps running even if you close terminal C. Stopping it requires `make down` (or `./rviz.bash down`).

```bash
# 1) 端末A(joy.bash) と 端末B(connect_zenoh.bash) をそれぞれ Ctrl+C で停止

# 2) コンテナを停止（rviz2 はここで止まる）
cd ~/aichallenge-racingkart
make down

# 3) 何も残っていないことを確認
docker compose ps                  # 何も残っていないこと
pgrep -af zenoh-bridge-ros2dds     # 何も出ないこと
pgrep -af joy_node                 # 何も出ないこと
```

(Steps: 1) stop terminal A (`joy.bash`) and terminal B (`connect_zenoh.bash`) with Ctrl+C; 2) stop the containers, which is where rviz2 stops; 3) confirm nothing is left: `docker compose ps` lists nothing and both `pgrep` commands print nothing.)

## Part 4: Using the Game Controller

### 4-1. Logicool F310

Remote operation uses the Logicool (Logitech) F310. The product page is [here](https://gaming.logicool.co.jp/ja-jp/products/gamepads/f310-gamepad.940-000137.html).

![Logicool F310](./images/f310-controller.png)

### 4-2. Button and axis assignments

The function of each button on the game controller is shown in the figure below.

![F310 joystick mapping (button/axis assignments)](./images/f310-button-mapping.png)
