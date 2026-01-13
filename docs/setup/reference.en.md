# Reference

## Incorporating Changes

When there are significant updates to the competition environment, announcements will be made accordingly. For reference, the following instructions are provided.

Update Docker

```bash
docker pull ghcr.io/automotiveaichallenge/autoware-universe:humble-latest
```

Update Repository

```sh
cd aichallenge2025 # path to aichallenge2025
git pull origin/main
```

## Installing AWSIM with Visualization

If you want to check the simulation screen of AWSIM, follow the steps in [this guide](../setup/visible-simulation.en.md) to install AWSIM with visualization.

## Setting up Three Terminals for Debugging (Reference)

To develop with three terminals for debugging, open the first terminal using `Alt+Ctrl+T` and then execute the following commands by pasting them with `Ctrl+Shift+V` and pressing `Enter`.

```bash
cd ~/aichallenge-racingkart
./docker_run.sh dev cpu
```

```bash
cd /aichallenge
bash run_simulator.bash
```

Open the second terminal using `Alt+Ctrl+T` and then execute the following commands by pasting them with `Ctrl+Shift+V` and pressing `Enter`.

```bash
cd ~/aichallenge-racingkart
./docker_run.sh dev cpu
```

```bash
cd /aichallenge
bash run_autoware.bash
```

Open the third terminal using `Alt+Ctrl+T` and then execute the following commands by pasting them with `Ctrl+Shift+V` and pressing `Enter`.

```bash
cd ~/aichallenge-racingkart
./docker_run.sh dev cpu
```

```bash
cd /aichallenge
ros2 topic pub --once /control/control_mode_request_topic std_msgs/msg/Bool '{data: true}' >/dev/null
```

When the screen below appears, the startup is complete. To terminate, press CTRL + C in each terminal.
![autoware](./images/autoware.png)
