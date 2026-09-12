# SW Division Submission Guide

## Online Environment

In the SW Division SIM Qualifying, scoring is conducted using an online environment equipped with a simulator and automatic scoring function. Follow the steps below to upload your packages to the online environment. After uploading, the simulation will automatically start and results will be displayed.

> Note: Screenshots on this page are from 2025.

## How Scoring and Ranking Work

Online scoring is not a simple lap-time ladder — it is a **head-to-head battle format**. Understanding the mechanism helps you plan your submission strategy.

- **Battle format**: Your submitted code (the CHALLENGER) races in the same session against the submitted code of a higher-ranked team (the defender), and the **finishing order** decides the winner.
- **Rating**: Your team's rating (Rate) goes up when you win and down when you lose, and the leaderboard is ordered by rating. A tie counts as a successful defense for the defender, and no rating changes.
- **Opponent selection (matchmaking)**: When submitting, you can choose how far above your own rank to challenge. Challenging a higher-ranked team yields a larger rating gain when you win.
    - A submission by the 1st-ranked team becomes a defense battle against an NPC.
    - Unranked teams enter the leaderboard after their first submission.

!!! note
    The exact rating formula, coefficients, and selectable opponent range may be adjusted by the organizers. Treat the online environment's own display as the source of truth for current behavior.

## Submission Lifecycle

Processing after upload has two stages: **build** (a Docker image is created from your code) and **execution** (the simulation battle runs). The STATUS shown for your submission follows these stages:

```text
Queued → Building → Running → Success
              └─ build failure ─┴─ run failure → Failed
```

Build failures and run failures have different causes and different places to look — see [If Failed](#if-failed) below.

## Submission Steps

Submit to the online environment using the following steps:

1. Compress source code

    - Run `./create_submit_file.bash` to compress the `aichallenge_submit` directory.
    - The compressed file is saved at `aichallenge-racingkart/submit/aichallenge_submit.tar.gz`.
    - See the [Participant Interface Contract (aichallenge-racingkart repository, in Japanese)](https://github.com/AutomotiveAIChallenge/aichallenge-racingkart/blob/main/docs/interface/participant-interface.md) for the structure and interfaces your submission must satisfy.

2. Verify operation in local evaluation environment

    See [Development Guide — Local Evaluation](../development/development-guide.en.md#local-evaluation) for details.

3. Submit to the online scoring environment

    Access the [online environment](https://aichallenge-board.jsae.or.jp).
    <img src="./images/topImage.png" width="100%">

    Log in from the "Login" button in the top right.
    <img src="./images/siteImage1.png" width="100%">

    Once logged in, upload `aichallenge_submit.tar.gz` using the "Submit Code" button. After uploading, the source code will be built and simulation will be run in sequence.
    <img src="./images/siteImage2.png" width="100%">

    On the upload screen, select the `aichallenge_submit.tar.gz` to upload. You can optionally add a comment. You can also change the rank range of the opponent to challenge — by default you battle the team one rank above you. Widening the range lets you challenge higher-ranked teams, with a larger rating gain if you win. Choose strategically.

    <img src="./images/siteImage3.png" width="100%">

## Checking Results

- After upload, your source code is built and then the simulation is run. You can check the STATUS of this submission under "Your Submissions" at the bottom of the screen. When processing goes normally it changes Queued → Building → Running → Success. The whole process takes about 30 minutes. If the build or the launch fails, "Failed" is displayed; check the logs and your submission (see [If Failed](#if-failed)).
- When the run in the online environment is finished, you can check the result in the Activity Timeline and the videos. Your rating goes up or down depending on the match result.
- Clicking the icon on the right of "Your Submissions" at the bottom of the page lets you view and download detailed run data such as lap times and logs.
    - You can check `result-summary.json`, the rosbag, and `autoware.log`.
    - "Copy Public Link" at the top right of the screen gives you a link for sharing on social media.

    <img src="./images/siteImage4.png" width="100%">

    <img src="./images/siteImage5.png" width="100%">

## If Failed

First determine whether it was a **build failure** or a **run failure**.

- **Failed during Building**: caused by dependency or build errors. Note that during the online build, dependencies that `rosdep` cannot resolve are **skipped without an error**, so a missing dependency may only surface at runtime rather than at build time. Always confirm your code builds and launches cleanly with a local `make eval` first.
- **Failed after reaching Running**: caused by launch failures or nodes crashing. Check `autoware.log` and the rosbag downloadable from the submission details.

- Check for package dependency issues

    - Verify that there are no missing dependencies in `package.xml`, `setup.py`, or `CMakeLists.txt`, depending on the language used.

- Check Docker

    - While `make eval` is running, you can enter the container with `make autoware-attach`.
    - To open the evaluation image directly, run `docker run --rm -it aichallenge-2025-eval bash` (the image name is set in `docker_build.sh`).

- Directories to check:

    - `/aichallenge/workspace/*`
    - `/autoware/install/*`

## Online Environment Pages

- "Overview" page (after login only)
    - Shows your team's rank information and submission history
- "Live" page
    - Shows rank information for all teams combined
- "Student Live" page
    - Shows rank information for the teams in the student class

- Description of each element
    - Video on the left
        - Replay of a match in which the code submitter (CHALLENGER, P1) beat the higher-ranked team (P2)
    - Video on the right
        - Replay of a match in which the higher-ranked team (defender, P2) beat the code submitter (P1)
    - Ranking Table
        - Shows the ranks of all teams
    - Activity Timeline
        - Shows the win/loss history
        - A sword icon marks a match won by the code submitter (CHALLENGER); a shield icon marks a match won by the higher-ranked team (defender)
    - Rate Transition
        - Shows how the rating has changed
    - Submissions
        - Shows the code submission history. You can check logs and download ROSBAGs here

<img src="./images/siteImage6.png" width="100%">
