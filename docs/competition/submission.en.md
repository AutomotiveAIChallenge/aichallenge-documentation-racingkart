# SW Division Submission Guide

## Online Environment

In the SW Division SIM Qualifying, scoring is conducted using an online environment equipped with a simulator and automatic scoring function. Follow the steps below to upload your packages to the online environment. After uploading, the simulation will automatically start and results will be displayed.

> Note: Screenshots on this page are from 2025.

## Submission Steps

Submit to the online environment using the following steps:

1. Compress source code

    - Run `./create_submit_file.bash` to compress the `aichallenge_submit` directory.
    - The compressed file is saved at `aichallenge-racingkart/submit/aichallenge_submit.tar.gz`.

2. Verify operation in local evaluation environment

    See [Development Guide — Local Evaluation](../development/development-guide.en.md#local-evaluation) for details.

3. Submit to the online scoring environment

    Access the [online environment](https://aichallenge-board.jsae.or.jp).
    <img src="./images/topImage.png" width="100%">

    Log in from the "Login" button in the top right.
    <img src="./images/siteImage1.png" width="100%">

    Once logged in, upload `aichallenge_submit.tar.gz` using the "Submit Code" button. After uploading, the source code will be built and simulation will be run in sequence.
    <img src="./images/siteImage2.png" width="100%">

    If successful, "Success" will be displayed.
    If the build fails, the launch fails, or the score is not output, "Failed" will be displayed. In this case, please re-upload as there may be an internal server error. Contact us via Slack if the problem persists.

    <img src="./images/siteImage3.png" width="100%">

## Checking Results

- After the race finishes in the online environment, you can check the latest rankings.
- Detailed race data including lap times and logs can be checked by clicking the button at the right end of the submission history.
    - You can check `result-summary.json`, rosbag, and `autoware.log`.

    <img src="./images/siteImage4.png" width="100%">

    <img src="./images/siteImage5.png" width="100%">

## If Failed

- Check for package dependency issues

    - Verify that there are no missing dependencies in `package.xml`, `setup.py`, or `CMakeLists.txt`, depending on the language used.

- Check Docker

    - Use the following command to check inside Docker and verify that everything is correctly installed and built in the required directories.

    - `docker run -it aichallenge-racingkart-eval:latest /bin/bash`

- Directories to check:

    - `/aichallenge/workspace/*`
    - `/autoware/install/*`
