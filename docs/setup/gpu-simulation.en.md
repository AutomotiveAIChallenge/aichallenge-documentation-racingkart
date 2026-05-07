# GPU Settings

First, follow [Setting Up the Environment](./introduction.en.md) to complete the setup.
If you encounter issues with AWSIM rendering or GPU configuration, refer to this page.

## GPU Environment Support

| Environment | Support | AWSIM Rendering | Sensors |
| ----------- | ------- | --------------- | ------- |
| **NVIDIA GPU present** | Supported | Yes | Yes |
| **Intel integrated GPU only (no NVIDIA)** | Supported | Yes | No |
| **No GPU** | Not supported | No | No |

- **NVIDIA GPU present**: AWSIM and Autoware can run with GPU acceleration.
- **Intel integrated GPU only**: AWSIM will launch, but sensor simulation does not work. This can be used to verify that AWSIM at least starts.
- **No GPU**: Not supported. AWSIM cannot be launched. If needed, try the headless mode described below.

## Checking .env { #env-check }

Check `~/aichallenge-racingkart/.env` and confirm it has the following settings. This is configured automatically by `setup.bash`. When `setup.bash` detects `/dev/nvidia0`, it automatically adds `docker-compose.gpu.yml` to `COMPOSE_FILE` in `.env`. If you are using an NVIDIA GPU but the settings differ, complete the NVIDIA GPU setup described below and then update `.env`.

```bash
# When using NVIDIA GPU (enable docker-compose.gpu.yml)
COMPOSE_FILE=docker-compose.yml:docker-compose.gpu.yml

# Intel integrated GPU only (leave the above line commented out)
# COMPOSE_FILE=docker-compose.yml:docker-compose.gpu.yml
```

## Installing GPU Drivers and Toolkits

**Common to all environments (NVIDIA GPU and Intel integrated GPU):**

- Install Vulkan

**NVIDIA GPU only:**

- Install NVIDIA driver (reboot recommended after installation)
- Install NVIDIA Container Toolkit

??? note "Vulkan installation steps"
    Run the following commands.

    ```bash
    sudo apt update
    sudo apt install -y libvulkan1
    ```

??? note "NVIDIA driver installation steps"
    ```bash
    # Add repository
    sudo add-apt-repository ppa:graphics-drivers/ppa

    # Update package list
    sudo apt update

    # Install
    sudo ubuntu-drivers install

    # Update package list
    sudo apt update

    # Verify installation with the command below.
    # The change is almost never reflected immediately, so a reboot (see below) is recommended.
    nvidia-smi
    ```

    The following command will reboot your PC — be careful if you do not want to power off at this point!
    ```bash
    # Reboot
    reboot
    ```

    ```bash
    # After reboot, verify the installation
    nvidia-smi
    ```

    ![nvidia-smi](./images/nvidia-smi.png)

??? note "NVIDIA Container Toolkit installation steps"
    Follow the official NVIDIA Container Toolkit instructions
    (`https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html`)
    to perform the installation.

    ```bash
    # Preparation
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
          && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
          && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
                sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
                sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    # Install
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker

    # Test the installation
    sudo docker run --rm --runtime=nvidia --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi

    # If the last command outputs something like the following, the installation was successful.
    # (The example below is quoted from the NVIDIA website)
    #
    # +-----------------------------------------------------------------------------+
    # | NVIDIA-SMI 450.51.06    Driver Version: 450.51.06    CUDA Version: 11.0     |
    # |-------------------------------+----------------------+----------------------+
    # | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    # | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    # |                               |                      |               MIG M. |
    # |===============================+======================+======================|
    # |   0  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
    # | N/A   34C    P8     9W /  70W |      0MiB / 15109MiB |      0%      Default |
    # |                               |                      |                  N/A |
    # +-------------------------------+----------------------+----------------------+
    # +-----------------------------------------------------------------------------+
    # | Processes:                                                                  |
    # |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    # |        ID   ID                                                   Usage      |
    # |=============================================================================|
    # |  No running processes found                                                 |
    # +-----------------------------------------------------------------------------+
    ```

!!! warning
    You do not need to follow steps that are already completed. The NVIDIA setup steps here are provided as a reference only — please refer to the official NVIDIA documentation for details.

## Verifying AWSIM Launch

Build and launch with the following commands.

```bash
cd aichallenge-racingkart
make simulator
```

If the simulator appears as shown below, the launch was successful.
![AWSIM-Autoware](./images/awsim.png)

Try launching Autoware as well.

```bash
cd aichallenge-racingkart
make autoware-build # Only needed if you have never built before
make autoware-simulator
```

If the following screen appears, the launch was successful.

![AWSIM-Autoware](./images/awsim-and-autoware.png)

Once you have confirmed, run the following command.

```bash
make down
```

## Headless Execution Without GPU (Not Officially Supported)

This is not officially supported, but AWSIM can be run in headless mode on a GPU-less environment with the following steps. The AWSIM window will not be displayed, but you can monitor the status in RViz.

1. In `aichallenge/run_simulator.bash`, add `--headless` to the `AWSIM.x86_64` launch options.
2. Remove `- /dev/dri:/dev/dri` from `docker-compose.yml`.
