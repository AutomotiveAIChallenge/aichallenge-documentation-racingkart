# Environment Updates

Announcements will be made whenever there is a significant update to the competition environment. Required steps will be included in each announcement, but the general procedures are described here for reference.

## Updating Docker

```bash
./setup.bash pull image
# or
docker pull ghcr.io/automotiveaichallenge/autoware-universe:humble-latest
```

## Updating Autoware

```bash
cd aichallenge-racingkart # path to aichallenge
git pull origin/main
```

## Updating AWSIM

```bash
./setup.bash download awsim
```

??? note "Manual download"
    Download `AWSIM.zip` from the SimPracticeFor2026 folder on OneDrive and extract it to `aichallenge-racingkart/aichallenge/simulator`.

    [:material-launch: Download AWSIM practice files](https://tier4inc-my.sharepoint.com/:f:/g/personal/taiki_tanaka_tier4_jp/IgCivzVKr4HDSbS1BpXObYmGASNQ6uv7iVjKc6ysyBMernE){ .md-button .md-button--primary  target="_blank" }

    Note: Only practice files are provided outside of the official competition period. Competition files may differ.

    Confirm that the executable exists at `aichallenge-racingkart/aichallenge/simulator/AWSIM/AWSIM.x86_64`.

    Set the file permissions as shown in the image below.

    ![Changing permissions](./images/awsim-permmision.png)
