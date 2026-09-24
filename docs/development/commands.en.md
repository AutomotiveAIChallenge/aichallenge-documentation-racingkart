# Command Reference

## setup.bash

Performs environment checks and initial setup.

| Command | Description |
|---|---|
| `./setup.bash` | Checks the environment and shows the next steps (same as `doctor`) |
| `./setup.bash doctor` | Checks the environment and prints a summary of the next steps |
| `./setup.bash bootstrap` | Installs Docker, clones the repository, and runs setup in one go (for setting up a new PC) |
| `./setup.bash pull image` | Pulls the Autoware base image with `docker pull` |
| `./setup.bash download awsim` | Downloads and extracts `AWSIM.zip` |
| `./setup.bash env` | Creates `.env` from `.env.example` |
| `./setup.bash network tune` | Persists the host settings for DDS (`rmem_max` and loopback multicast; requires sudo) |
| `./setup.bash network if [name]` | Adds a network interface to `cyclonedds.xml`; without a name, removes all interfaces that were added by this script |

## create_submit_file.bash

Compresses `aichallenge_submit/` into a submission file. The output is `submit/aichallenge_submit.tar.gz`.

```bash
./create_submit_file.bash
```

## docker_build.sh

Builds Docker images. Build logs are saved under `output/docker/`.

| Command | Description |
|---|---|
| `./docker_build.sh dev` | Builds the development image (`aichallenge-2025-dev`) |
| `./docker_build.sh eval` | Builds the evaluation image with the submission file embedded (`aichallenge-2025-eval`); always a full build with `--no-cache` |
| `./docker_build.sh eval --submit <path>` | Builds using the submission file at `<path>` (default: `submit/aichallenge_submit.tar.gz`) |

## make commands

### Build, start, and stop

| Command | Description |
|---|---|
| `make autoware-build` | Builds the ROS workspace (`aichallenge/workspace/`) |
| `make dev` | Starts AWSIM + Autoware for development (shorthand for `simulator` + `autoware-simulator`) |
| `make dev2` | Starts AWSIM + 2 × Autoware for development |
| `make dev3` | Starts AWSIM + 3 × Autoware for development |
| `make dev4` | Starts AWSIM + 4 × Autoware for development |
| `make e2e` | Starts AWSIM + Autoware for End to End practice (with 2 NPCs; also use this to check before submitting) |
| `make eval` | Starts AWSIM + Autoware for evaluation |
| `make gate1` | Starts the safety gate scenario (obstacle stop) |
| `make gate2` | Starts the safety gate scenario (overtaking) |
| `make gate3` | Starts the safety gate scenario (lane keeping) |
| `make down` | Stops and removes all running containers |
| `make down_all` | Force-removes all Docker containers on the host |
| `make ps` | Lists running containers |
| `make autoware-attach` | Opens bash in an existing container |
| `make autoware-bash` | Opens bash in a new container |

### Starting individual services

| Command | Description |
|---|---|
| `make simulator` | Starts AWSIM only |
| `make simulator-dev2` | Starts AWSIM only (for 2 vehicles) |
| `make simulator-dev3` | Starts AWSIM only (for 3 vehicles) |
| `make simulator-dev4` | Starts AWSIM only (for 4 vehicles) |
| `make simulator-e2e-final` | Starts AWSIM only (End to End finals settings) |
| `make simulator-s2r-final` | Starts AWSIM only (Sim to Real finals settings) |
| `make autoware-simulator` | Starts Autoware only (for the simulator) |
| `make autoware-vehicle` | Starts Autoware only (for the real vehicle) |
| `make driver` | Starts the real-vehicle interface (`racing_kart_interface`) |
| `make zenoh` | Starts Zenoh (remote connection to the real vehicle) |
| `make rviz2` | Starts RViz2 |
| `make autoware-driver-zenoh` | Starts `driver` + `autoware` + `zenoh` together (for the real vehicle) |

`make simulator-<mode>` runs `aichallenge/simulator_scripts/<mode>.sh`. For the list of modes and their settings, see [Simulator launch modes](../specifications/simulator.en.md#launch-modes).

### Sending commands

| Command | Description |
|---|---|
| `make autoware-request-control` | Sends the control mode request for autonomous driving |
| `make autoware-request-initialpose` | Sends the request to set the initial pose |
| `make awsim-request-reset` | Resets the simulator |
| `make awsim-request-start` | Sends the race start command to the simulator |

### Other

| Command | Description |
|---|---|
| `make download` | Downloads submission data (can be specified with `SUBMISSION_ID=<id>`) |
