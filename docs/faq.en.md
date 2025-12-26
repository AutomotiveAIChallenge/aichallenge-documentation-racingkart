# FAQ

!!! warning

    Many issues can be resolved using ChatGPT or Google search. For questions that cannot be resolved, please include and attach excerpts of error logs.

## Environment Setup

### <u>The communication between AWSIM and Autoware is unstable.</u>

When testing locally, setting `ROS_LOCALHOST_ONLY=1` in all terminals can improve communication speed. Add the following lines to your `.bashrc`.

```bash
export ROS_LOCALHOST_ONLY=1
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

if [ ! -e /tmp/cycloneDDS_configured ]; then
    sudo sysctl -w net.core.rmem_max=2147483647
    sudo ip link set lo multicast on
    touch /tmp/cycloneDDS_configured
fi
```

For a dual-PC setup (Windows+Linux or Linux+Linux), set `ROS_LOCALHOST_ONLY=0`.

Note:

- After OS startup, you will need to enter the password when starting the terminal and execute `sudo ip link set lo multicast on` for the first time.
- Always track changes by using commands like `echo $ROS_LOCALHOST_ONLY` to avoid forgetting modifications in `.bashrc`.
- Mixed use of `ROS_LOCALHOST_ONLY=1` and `ROS_LOCALHOST_ONLY=0` will prevent container communication.
- Ensure that `ROS_LOCALHOST_ONLY` is not hard-coded in the executable.

---

### <u>ros2 topic list does not display.</u>

Ensure that the `ROS_DOMAIN_ID` matches on your machine (this is not an issue if you haven't set `ROS_DOMAIN_ID`). Also, ensure ROS2 is sourced correctly.

---

### <u>Using AWSIM on Windows and Autoware on Ubuntu, ros2 topic list does not display.</u>

Allow communication through the Windows Firewall. Also, execute `ros2 daemon stop` and `ros2 daemon start` to ensure no unnecessary processes are running, then restart.

---

### <u>Rocker does not start.</u>

First, verify that Rocker is installed. If it is installed but does not start, check the permissions. It has been reported that differing account types and permissions when building and running the image can cause issues.

---

### <u>AWSIM terminates with a core dump.</u>

If AWSIM terminates with a core dump immediately after startup, your GPU may be out of memory. Check the GPU memory usage with `nvidia-smi` to ensure it is not at its limit. A GPU with at least 11GB of memory is recommended.

---

### <u>Unity cannot be loaded when running `./run_simulator.bash`.</u>

If Unity fails to load when running the simulator (e.g., in Getting Started: TinyLiDARNet) and the simulator screen turns entirely pink as shown below, the container may not be recognizing the GPU.

![Unity pink screen](https://github.com/user-attachments/assets/2e9b5b06-18a3-476d-bf32-4b17d78f322e)

Please ensure that `nvidia-smi` works inside the container before running the simulator. If `nvidia-smi` does not work, check your NVIDIA driver installation and Docker GPU configuration.

---

### <u>I only have a Windows PC with a GPU.</u>

The official support is for the configuration listed on the HP website, so detailed guidance cannot be provided, but generally, the following methods are possible:

The key is to "prepare an environment to run Autoware," which may involve issues related to performance, package availability, and host-container communication settings. Possible solutions include:

- Setting up Ubuntu in a dual-boot configuration.
- Using a VM on Windows to run Ubuntu (Hyper-V, VirtualBox, VMware, etc.).
- Setting up Ubuntu on WSL2.
- Setting up a Docker environment on Windows and running the Autoware image directly.
- Building the environment in the cloud (some past participants used AWS).

---

### <u>AWSIM appears but Rviz shows a black screen when set up on AWS.</u>

There have been cases where running `sudo apt upgrade` resolved the issue. Additionally, there is a [similar question](https://github.com/ros2/rviz/issues/948) in a past issue that might be helpful.

---

### <u>`docker_run.sh: line 35: rocker: command not found` appears.</u>

Please install Rocker as described [here](setup/docker.en.md).

---

### <u>`WARNING unable to detect os for base image 'aichallenge-2025-dev', maybe the base image does not exist` appears.</u>

Please build the Docker image.

---

### <u>Unable to pull Docker.</u>

Please restart Docker with `newgrp docker` or `sudo service docker restart`, or restart Ubuntu.

---

## Operations

### ROS

#### <u>I get a no module named \* error when creating a package with Python and running it.</u>

Refer to [this guide](https://zenn.dev/tasada038/articles/5d8ba66aa34b85#setup.py%E3%81%ABsubmodules%E3%81%A8%E3%81%97%E3%81%A6%E3%83%91%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B8%E3%82%92%E8%BF%BD%E5%8A%A0%E3%81%99%E3%82%8B).

---

#### <u>What command should I use to check the type of a topic?</u>

Use `ros2 topic info -v fuga_topic` to check the type of a topic, or if you can identify the node, use `ros2 node info hoge-node`. For more information about ROS commands, searching for "ROS2 commands" online may also help.

---

### Autoware

#### <u>Maps and routes are not displayed in Rviz.</u>

Ensure that the map data is placed in the correct location and is valid.

---

#### <u>I don't know how to improve Autoware for participation.</u>

Methods include adjusting parameters, improving nodes, or replacing nodes in Autoware. Basic configurations of Autoware can be found on the website or [here](https://automotiveaichallenge.github.io/aichallenge2023-integ/customize/index.html). Additionally, [this external article](https://qiita.com/h_bog/items/86fba5b94b2148c4d9da) might be helpful.

---

#### <u>Please explain about Behavior Path/Motion Planner.</u>

The behavior planner primarily functions for general roads (ODD3 and above), considering traffic rules like stop lines, crosswalks, and signal stops. It does not optimize avoidance functions. On the other hand, the motion planner functions for limited areas (ODD2 and below), handling basic driving functionalities such as obstacle avoidance, stopping, and speed optimization without using signals or map information.

---

#### <u>Please explain Autoware's avoidance behavior.</u>

There are two types of avoidance: behavior path and obstacle avoidance. By default, obstacle avoidance is off and only path smoothing is performed. The default setting is to avoid using the behavior path, but the default avoidance targets are only cars and trucks.

---

#### <u>Please explain the center point.</u>

The center point detects cars, trucks, and pedestrians, but not untagged objects like cardboard boxes. Currently, Autoware requires object data for planning, and the default configuration using center point can lead to two issues:

1. If the center point fails, planning cannot generate a path.
2. Clustering-based obstacle detection results are erased during data association.

Although Autoware mini is the ideal perception configuration, understanding these issues and selectively implementing nodes is challenging. Ensuring the center point functions correctly may be important. [Reference](https://autowarefoundation.github.io/autoware.universe/main/perception/autoware_lidar_centerpoint/)

---

### AWSIM

#### <u>How can I reset the car to the initial position?</u>

Currently, the only way to do this is by restarting AWSIM.

---

#### <u>AWSIM operation is unstable.</u>

This may be due to insufficient GPU performance. If using a high-performance GPU is not feasible, setting the time scale to about 0.5 using the slider at the bottom of the AWSIM screen may stabilize operation.

---

#### <u>I want to tune the MPC. Are the model parameters (delay and time constants) used in this AWSIM disclosed?</u>

The delay and time constants are neither measured nor disclosed, but the basic specifications are available [here](./specifications/simulator.en.md).

---

## General Competition Questions

### <u>Is it possible to add extra sensors?</u>

To ensure all participants face the same conditions and difficulty, the addition of new sensors is not allowed.
