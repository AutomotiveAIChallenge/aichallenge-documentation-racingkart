# Setting Up the Environment

This chapter explains how to set up the development and execution environment for the Autonomous Driving AI Challenge 2026 (Racing Kart). It covers verifying the recommended environment, preparing the workspace, and launching Docker and AWSIM.

??? info "Changes for 2025 participants"
      - `rocker` is now limited to GUI forwarding; process management uses docker compose.
      - Individual setup steps have been consolidated into a single batch installation procedure.

## Environment Setup

First, install the curl package.

```bash
sudo apt update
sudo apt install curl
```

Then run the following command, which performs everything from environment setup to a simulator launch test in one shot.

```bash
curl -fsSL "https://raw.githubusercontent.com/AutomotiveAIChallenge/aichallenge-racingkart/main/setup.bash" | bash
```

!!! tip "Re-running the setup"
    If you already have the repository, you can run the script directly instead of using `curl`.

    ```bash
    cd ~/aichallenge-racingkart
    ./setup.bash bootstrap
    ```

What this single command does (regarding the virtual environment)

The following describes what `setup.bash` performs interactively, step by step. Open only the steps you need to review.

??? note "1. :material-package: Install required packages"
    Installs the essential base packages.

    ```bash
    sudo apt update
    sudo apt install -y python3-pip ca-certificates curl gnupg
    ```

??? note "2. :material-docker: Install Docker"
    Adds the official Docker repository and installs Docker itself.

    ```bash
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
    Verify that Docker is working correctly.

    ```bash
    sudo docker run hello-world
    ```
    If you see "Hello from Docker!", the installation was successful.

??? note "3. :material-language-python: Install rocker"
    Installs rocker (used for GUI forwarding) and adds it to PATH.

    ```bash
    pip install rocker
    ```

    If `~/.local/bin` is not in your PATH, add it.

    ```bash
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

??? note "4. :material-account-group: Register Docker group"
    Adds your user to the Docker group so you can run Docker without `sudo`.

    ```bash
    sudo usermod -aG docker $USER
    newgrp docker
    ```

??? note "5. :material-folder-open: Prepare repository"
    Clones the competition repository and runs a pre-check.

    ```bash
    cd ~
    git clone https://github.com/AutomotiveAIChallenge/aichallenge-racingkart.git
    cd ~/aichallenge-racingkart
    ```

??? note "6. :material-security: Verify repository"
    Checks that the repository exists correctly.

    ```bash
    ./setup.bash doctor
    ```

??? note "7. :material-cloud-download: Pull Autoware image"
    Pulls the Autoware base image required for execution.

    ```bash
    docker pull ghcr.io/automotiveaichallenge/autoware-universe:humble-latest
    docker images
    ```

    If the Docker image was downloaded successfully, you will see output like this:

    ```txt
    REPOSITORY                                        TAG                       IMAGE ID       CREATED         SIZE
    ghcr.io/automotiveaichallenge/autoware-universe   humble-latest             30c59f3fb415   13 days ago     8.84GB
    ```

??? note "8. :material-download: Download/extract AWSIM data"
    Downloads AWSIM from SharePoint and extracts it to the designated directory with execute permission.

    1. Download the latest `AWSIM.zip` from the link below.

    [:material-launch: Download AWSIM](https://tier4inc-my.sharepoint.com/:f:/g/personal/taiki_tanaka_tier4_jp/EopMoY32mnNLhPVHWZkkow4B5M71TLlFpS6xrOE7Zfhuug){ .md-button .md-button--primary  target="_blank" }

    ```bash
    mkdir -p ~/aichallenge-racingkart/aichallenge/simulator
    unzip ~/Downloads/AWSIM.zip -d ~/aichallenge-racingkart/aichallenge/simulator
    chmod +x ~/aichallenge-racingkart/aichallenge/simulator/AWSIM/AWSIM.x86_64
    ```

    2. Confirm the executable exists at the following path.

    ```bash
    ls ~/aichallenge-racingkart/aichallenge/simulator/AWSIM/AWSIM.x86_64
    ```

    3. Refer to the figure below for the expected permissions.

    ![Permission change](./images/awsim-permmision.png)

    For GPU use, extract `AWSIM_GPU_**.zip` instead.

??? note "9. :material-hammer: Build development image"
    Builds the Docker image for development.

    ```bash
    cd ~/aichallenge-racingkart
    ./docker_build.sh dev
    ```

??? note "10. :material-book-education: Build workspace"
    Builds the Autoware workspace.

    ```bash
    cd ~/aichallenge-racingkart
    make autoware-build
    ```

??? note "11. :material-power: Launch AWSIM + Autoware → confirm stop with `make down`"
    Launches the simulator and Autoware, then stops them after confirming.

    ```bash
    cd ~/aichallenge-racingkart
    make dev
    make down
    ```

## Reading the Setup Screen

- When `Select branch [default: main]:` appears, select `main` (or just press `Enter`)
- `[y/N]` confirms whether to run each step (normally answer `y`)
- `Starting execution...` means setup is running automatically
- `To stop: make down` means the launch check is complete

```.bash
[setup] ℹ️ Bootstrap mode (fresh host)
[setup] Available branches (remote):
[setup]   1) dev
[setup] Select branch [default: main]: main
[setup] ℹ️ Planned steps (answer y/N for each, then execution starts):
[setup]   1) Install base packages (apt)
[setup]   2) Install Docker (if missing)
[setup]   3) Install rocker (pip)
[setup]   4) Add user to docker group (recommended)
[setup]   5) Clone/update repository (branch=main) -> $USER/aichallenge-racingkart
[setup]   6) Repo preflight: ./setup.bash doctor (requires repo)
[setup]   7) Create .env (GPU/CPU auto-detect)
[setup]   8) Pull Autoware base image (requires repo)
[setup]   9) Download AWSIM.zip and extract (requires repo)
[setup]  10) Build dev image: ./docker_build.sh dev (requires repo)
[setup]  11) make autoware-build (requires repo)
[setup]  12) make dev DOMAIN_ID=1 (requires repo)
```

When `[y/N]` appears, enter `y` if there are no issues.

```.bash
[setup] Install base packages (apt) [y/N]: y
[setup] Install Docker (if missing) [y/N]: y
[setup] Add user to docker group (recommended) [y/N]: y
[setup] Clone/update repository (branch=main) -> $USER/aichallenge-racingkart/aichallenge-racingkart [y/N]: y
[setup] Run repo preflight: ./setup.bash doctor [y/N]: y
[setup] Pull Autoware base image [y/N]: y
[setup] Download AWSIM.zip and extract [y/N]: y
[setup] Build dev image: ./docker_build.sh dev [y/N]: y
[setup] Run make autoware-build (this can take a while) [y/N]: y
[setup] Run make dev DOMAIN_ID=1 [y/N]: y
[setup] ℹ️ Starting execution...
[setup] ℹ️ Running: Install base packages (apt)
```

After this, just wait about 5 minutes. Grab a coffee while you wait.

:coffee:

When setup is complete, AWSIM and Autoware will launch with output like the following.

```bash
Start dev simulation (AWSIM + Autoware, DOMAIN_ID=1)
make[1]: ディレクトリ '$USER/aichallenge-racingkart' に入ります
Start AWSIM
SIM_MODE=dev docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d simulator
[+] up 1/1
make[1]: ディレクトリ '$USER/aichallenge-racingkart/aichallenge-racingkart' から出ます         0.5s
make[1]: ディレクトリ '$USER/aichallenge-racingkart/aichallenge-racingkart' に入ります
Start Autoware for AWSIM
RUN_MODE=awsim DOMAIN_ID=1 docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d autoware
[+] up 1/1
 ✔ Container aichallenge-2026-autoware-1 Created                           0.2s
make[1]: ディレクトリ '$USER/aichallenge-racingkart/aichallenge-racingkart' から出ます
To stop: make down  (docker compose down --remove-orphans)
```

AWSIM and Autoware are now running.
![autoware-awsim](./images/autoware-awsim.png)
To stop, run the following command.

```bash
cd ~/aichallenge-racingkart
make down
```

This completes the environment setup and operation check.

- If AWSIM does not launch or has rendering issues, check your GPU settings.
    - [GPU Settings](./gpu-simulation.en.md)
- If you are ready to start developing, see the development guide.
    - [Development Guide](../development/development-guide.en.md)
