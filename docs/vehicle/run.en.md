# Launching the Real Vehicle

This page describes how to run the code you developed for the simulator on the real vehicle, using an ECU that has already been set up.

For the initial setup of the ECU (MiniPC) itself, see [Initial ECU Setup](ecu-setup.en.md). Setting up and operating the remote PC is covered in [Remote Operation](remote.en.md).

## Part 1: Pre-Run Configuration and Launch

Unlike the simulator, on the real vehicle you must always check the following before driving.

### 1-1. Configuring `.env`

`.env` is not tracked by git; it is generated from `.env.example` by `./setup.bash bootstrap` (or `./setup.bash env`).
After generation, the following four items must first be edited by hand. If you use V2X position sharing, the items described further below are also required.

| Variable | Initial value in `.env.example` | Setting required on the real vehicle |
| --- | --- | --- |
| `VEHICLE_ID` | `A0` | The kart number to drive (`A1`,`A2`,`A3`,`A5`,`A6`,`A7`,`A8`). This value determines the zenoh connection port (`vehicle/run_zenoh.bash`) |
| `NTRIP_USERNAME` | `your_username` | Account for the RTK correction service (NTRIP). If it is not set, you will not get an RTK Fix and localization accuracy will be poor |
| `NTRIP_PASSWORD` | `your_password` | Same as above |
| `RACING_KART_INTERFACE_DIR` | `/home/tier4/racing_kart_interface` | The actual location of racing_kart_interface. **It must be an absolute path** (because `colcon --symlink-install` contains absolute symlinks). If this is wrong, rosbag recording also fails |

`ROS_DOMAIN_ID` can stay at the default `1`. `TEAM_NAME` is included in `.env.example` but is not referenced when launching the real vehicle, so it can also stay at its initial value.

`HOST_UID` / `HOST_GID` / `HOST_GID_DIALOUT` / `HOST_GID_INPUT` and `COMPOSE_FILE` (GPU detection) are set automatically from measured values by `./setup.bash env`, so you normally do not touch them.

If you use V2X position sharing, also set the following items in `.env`. For placing the certificates, see section 4-4 of [Initial ECU Setup](ecu-setup.en.md).

| Variable | Initial value in `.env.example` | Setting required on the real vehicle |
| --- | --- | --- |
| `V2X_VEHICLE_ID` | `d1` | This vehicle's V2X ID. It is rejected by the broker unless it matches the CN of `/etc/v2x/tls/kart.crt` |
| `V2X_VEHICLE_IDS` | `d1,d2,d3,d4` | Comma-separated IDs of all vehicles that may take part in the run. Use the same value on every kart. Position data received from IDs not listed here is discarded |
| `V2X_BROKER_HOST` | `v2x-mqtt-cctb.dev.aichallenge-board.jsae.or.jp` | The MQTT broker to connect to. Match the value distributed together with the certificates |
| `V2X_BROKER_PORT` | `8883` | Port for the TLS connection. It is not `1883` |
| `V2X_TLS_DIR` | `/etc/v2x/tls` | Certificate directory on the host. On the container side it is always mounted read-only at `/etc/v2x/tls`, so changing this value does not change the path inside the container |
| `V2X_MQTT_TLS_CA_FILE` / `_CERT_FILE` / `_KEY_FILE` | `/etc/v2x/tls/ca.crt` etc. | Paths as seen from inside the container. Keep the initial values even if you change `V2X_TLS_DIR`. Unless all three are set, the whole TLS configuration is disabled |

`VEHICLE_ID` (the kart number, which determines the zenoh connection port) and `V2X_VEHICLE_ID` (this vehicle's own V2X ID, i.e. the certificate CN) are different things. Before driving, prepare and share a table mapping kart number, `V2X_VEHICLE_ID` and certificate CN for every participating kart to avoid mix-ups.

### 1-2. Correcting the IMU Bias

Measure the IMU gyro bias for each vehicle and update the `imu_corrector` parameters. `/sensing/imu/imu_raw` is not published unless driver / autoware are running, so launch once with "1-3. Launching the Vehicle" before measuring.

The target file is `aichallenge/workspace/src/aichallenge_submit/imu_corrector/config/imu_corrector.param.yaml`.

With the vehicle stationary, observe `angular_velocity` on `/sensing/imu/imu_raw` and write the mean value of each axis directly into `angular_velocity_offset_x` / `_y` / `_z` (no sign inversion is needed). Because the workspace is built with `--symlink-install`, no rebuild is needed; restarting autoware applies the change.

### 1-3. Launching the Vehicle

Operations during a run slot are consolidated into the vehicle console launched with `make vehicle-tui`. It is a TUI running in tmux that lets you run the pre-checks, submission download, build, driver launch and shutdown in order from a single screen. Internally it calls the following make targets and `setup_check.sh`, so you may also run them individually.

```bash
# 提出物データを aichallenge/workspace/src/ に取得（認証情報は対話入力）
make download                       # 提出物の一覧を表示して選択
make download SUBMISSION_ID=<id>    # 特定の提出物を指定（一覧をスキップ）

# 取得／持ち込んだコードをビルド
make autoware-build

# rosbag を記録する場合（セットアップ確認込み。実車両では基本こちら）
make autoware-driver-zenoh-rosbag

# rosbag を記録しない場合（セットアップ確認は実行されない）
make autoware-driver-zenoh
```

(Comments in the block above, in order: fetch the submission data into `aichallenge/workspace/src/` (credentials are entered interactively); `make download` lists the submissions and lets you choose; `SUBMISSION_ID=<id>` selects a specific submission and skips the list; build the fetched or brought-in code; to record rosbags (includes the setup check; this is the normal choice on the real vehicle); without rosbag recording (the setup check is not run).)

`make autoware-driver-zenoh-rosbag` runs the following in order:

1. `./setup_check.sh --phase preflight` (pre-launch check)
2. Launch `driver` + `autoware` + `rosbag`
3. Wait 15 seconds, then launch `zenoh`
4. `./setup_check.sh --phase runtime` (post-launch check)

`make autoware-driver-zenoh` only launches `driver` + `autoware`, waits 15 seconds and launches `zenoh`; **the setup check is not run**. If you launched with this target, check separately with `make setup-vehicle`.

rosbags record all topics (`-a --include-hidden-topics`) in mcap format, split every 60 seconds, to `output/<timestamp>/d<ROS_DOMAIN_ID>/rosbag2_all/`. The recording log is `rosbag.log` in the same directory.

### 1-4. Shutdown Procedure

```bash
make ps      # 稼働中のコンテナ確認
make down    # 全コンテナ停止（rosbag もここで finalize される）
```

(`make ps` lists the running containers; `make down` stops all containers, which is also when the rosbag is finalized.)

## Part 2: Setup Check Script

`make autoware-driver-zenoh-rosbag` runs both the preflight and runtime phases automatically, so you normally do not need to run them individually. If you launched with `make autoware-driver-zenoh`, or want to run the check on its own, use `make setup-vehicle` (it runs both phases, so run it while autoware is up).

The preflight (pre-launch) phase checks the following:

1. **Hardware devices** - CAN, VCU, GNSS/RTK
2. **Network and communication** - internet connection, DNS resolution, Zenoh server reachability
3. **Docker and environment** - Docker running, images present, permission settings
4. **Known-issue prevention checks** - preventive items extracted from past experiments
5. **Readiness** - repository root, git branch

The runtime (post-launch) phase checks the following:

1. **Hardware connectivity** - CAN interface UP state and frame rate
2. **Docker services** - whether the required compose services are running
3. **GNSS/RTK status** - RTK Fix status on `/sensing/gnss/navpvt`
4. **ROS topic output** - VCU status / command, Autoware vehicle status

The expected result of each item, manual check commands, troubleshooting, and the final pre-run checklist are collected in the repository's [vehicle/setup_check.md](https://github.com/AutomotiveAIChallenge/aichallenge-racingkart/blob/main/vehicle/setup_check.md).

## Part 3: Troubleshooting

### 3-1. When the ECU Cannot Communicate with the Motor or VCU

Take the following steps in order, then re-run `make autoware-driver-zenoh-rosbag`.

1. Stop all containers with `make down_all`
2. Unplug and re-plug the USB cable
3. Power-cycle the vehicle battery
4. Run `make autoware-driver-zenoh-rosbag`
