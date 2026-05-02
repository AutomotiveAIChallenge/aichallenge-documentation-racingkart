# Command Reference

## setup.bash

Performs environment checks and initial setup.

| Command | Description |
|---|---|
| `./setup.bash` | Checks the environment and shows the next steps (same as `doctor`) |
| `./setup.bash doctor` | Checks the environment and prints a summary of the next steps |
| `./setup.bash bootstrap` | Installs Docker, clones the repository, and runs setup in one shot (for new machines) |
| `./setup.bash pull image` | Pulls the Autoware base image via `docker pull` |
| `./setup.bash download awsim` | Downloads and extracts `AWSIM.zip` |
| `./setup.bash env` | Creates `.env` from `.env.example` |

## create_submit_file.bash

Compresses `aichallenge_submit/` into a submission archive. Output: `submit/aichallenge_submit.tar.gz`.

```bash
./create_submit_file.bash
```

## docker_build.sh

Builds Docker images. Build logs are saved under `output/docker/`.

| Command | Description |
|---|---|
| `./docker_build.sh dev` | Builds the development image (`aichallenge-2025-dev`) |
| `./docker_build.sh eval` | Builds the evaluation image (`aichallenge-2025-eval`) — always a full rebuild with `--no-cache` |
| `./docker_build.sh eval --submit <path>` | Builds the evaluation image with a submission archive embedded |

## run_parallel_submissions.bash

Evaluates multiple submission archives simultaneously. Accepts 1–4 archives (`aichallenge_submit.tar.gz`) and runs each on a separate Domain ID (`d1`–`d4`).

| Command | Description |
|---|---|
| `./run_parallel_submissions.bash --submit <tar1> [<tar2> ...]` | Evaluates 1–4 submissions in parallel |
| `./run_parallel_submissions.bash down` | Stops all running containers |

Logs and results are saved under `output/<timestamp>/d<domain_id>/`.

## make commands

### Build, start, and stop

| Command | Description |
|---|---|
| `make autoware-build` | Builds the ROS workspace (`aichallenge/workspace/`) |
| `make dev` | Starts AWSIM + Autoware for development (shorthand for `simulator` + `autoware-simulator`) |
| `make eval` | Starts AWSIM + Autoware for evaluation |
| `make down` | Stops and removes all running containers |
| `make down_all` | Force-removes all Docker containers on the host |
| `make ps` | Lists running containers |

### Starting individual services

| Command | Description |
|---|---|
| `make simulator` | Starts AWSIM only |
| `make autoware-simulator` | Starts Autoware only (simulation mode) |
| `make autoware-vehicle` | Starts Autoware only (real vehicle mode) |
| `make driver` | Starts the vehicle interface (`racing_kart_interface`) |
| `make zenoh` | Starts Zenoh (remote vehicle connection) |
| `make rviz2` | Starts RViz2 |
| `make autoware-driver-zenoh` | Starts `driver` + `autoware` + `zenoh` together (real vehicle use) |

### Sending commands

| Command | Description |
|---|---|
| `make autoware-request-initialpose` | Sends a request to set the initial pose |
| `make autoware-request-control` | Sends a request to enable autonomous driving control mode |
| `make simulator-reset` | Resets the simulator |

### Other

| Command | Description |
|---|---|
| `make download` | Downloads submission data (optionally specify `SUBMISSION_ID=<id>`) |
