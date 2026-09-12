# Recommended Environment

We recommend the following specifications for the PC you use in this competition.
Items marked "recommended" are not strictly required for the software to run. However, if you run on a PC with lower specifications than recommended, execution speed on the ROS 2 side may become unstable, and behavior may change significantly from one simulation run to the next.

!!! warning

    If you only have a Windows environment, please install Ubuntu 22.04. It is possible to install Ubuntu on the same disk as Windows, but if you are not familiar with the process you may damage your Windows installation, so we strongly recommend buying a new external or internal SSD and installing Ubuntu there.

    Ubuntu 24.04 may work, but it is not officially supported.

    WSL can also run the stack in headless mode (without the simulator window), but it is not officially supported.

!!! info

    For guidance on installing Ubuntu, [this article](https://qiita.com/kiwsdiv/items/1fa6cf451225492b33d8) may be helpful.

## GPU Environment Support

| Environment | AWSIM Rendering | Camera/LiDAR |
| ---- |  --------- | -------- |
| **NVIDIA GPU** |  Yes | Yes |
| **Intel integrated GPU only** |  Yes | No |
| **No GPU** |  No | No |

- **NVIDIA GPU**: AWSIM and Autoware can run with GPU acceleration. This environment is required for the End to End AI division.
- **Intel integrated GPU only**: AWSIM launches, but the Camera/LiDAR sensors cannot be used. This environment is sufficient for the Sim to Real SW division.
- **No GPU**: The stack can run in headless mode, in which the AWSIM window is not displayed. You can do a minimal operation check in RViz.

## PC Specifications (Guideline)

The following are the PC specifications required for development and execution. For the specifications of the PCs actually used in the competition, see [Specifications / Hardware](../specifications/hardware.en.md).

- OS: Ubuntu 22.04
- CPU:
    - 11th Gen Intel Core i5 (8 cores) or higher (minimum)
    - 13th Gen Intel Core i7 (8 cores) or higher (recommended)
- GPU:
    - With an NVIDIA GPU
        - GTX 1650 or higher (minimum)
        - RTX 3060 or higher (recommended)
    - With an Intel integrated GPU only
        - Iris Xe Graphics or higher
    - Without a GPU
        - None
- Memory:
    - 4 GB or more (minimum)
    - 8 GB or more (recommended)
- SSD: 60 GB or more

If you train machine learning models for the End to End AI division, we additionally recommend an NVIDIA GPU with the following performance:

- 4 GB VRAM or more (e.g. GTX 1650, RTX 3050) (minimum)
- 8 GB VRAM or more (e.g. RTX 3060, RTX 4060) (recommended)

## Checking Your Environment

- The specifications above are guidelines. To check whether your own environment can run the stack, actually try it by following [Setting Up the Environment](./introduction.en.md).
- While Autoware is running, check that each process runs at the expected rate.
    - The FPS shown at the top right of the AWSIM window is 30 FPS or higher (60 FPS ideally)
    - The frequency of the `/control/command/control_cmd` topic, shown by the command below, is about 40 Hz (when the control algorithm is MPC, the default setting; about 100 Hz when the control algorithm is SimplePurePursuit)

        ```bash
        make autoware-bash
        ros2 topic hz /control/command/control_cmd -w 10
        ```
