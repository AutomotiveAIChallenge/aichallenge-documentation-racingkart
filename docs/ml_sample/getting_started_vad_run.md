# Getting started: VAD Plannerの実行

このドキュメントでは、Gemini APIとAWSIMを用いて、VAD Plannerを動かす方法について説明します。

## AWSIMの実行

- [AWSIM側の準備](./getting_started_vlm_setup.md#awsim側の準備)にて作成したdocker container内で、`./run_evaluation.bash`を実行しましょう。
  - scaleは0.20程度に変更しましょう。(Geminiが5秒に1回しか推論できないため。)

![camera_awsim_after](../assets/camera_awsim_after.png)

## VAD Plannerの実行

### VADの実行

- [VAD Planner環境側の準備](./getting_started_vad_setup.md#vad-planner環境側の準備)で作成したdocker container内で、以下を実行しましょう。
  - 以下のコマンドを実行し、VAD Plannerを動かしてみてください。

```sh
cd e2e-utils-beta;source install/setup.bash
```

```sh
ros2 launch vad_aic_launch vad_aic.launch.xml use_sim_time:=true
```

### trajectory selectorの実行

- [VAD Planner環境側の準備](./getting_started_vad_setup.md#vad-planner環境側の準備)で作成したdocker container内に、もう一つterminalを立ち上げます。

```sh
docker exec -it aichallenge-e2e-utils-vad /bin/bash
```

- 以下を実行し、trajectory selectorを起動してください。

```sh
cd e2e-utils-beta;source install/setup.bash
```

```sh
cd e2e-utils-beta/src/vlm_trajectory_selector;source .venv/bin/activate
```

```sh
python trajectory_selector.py --ros-args -p input_topic:="/planning/vad/trajectories_base" -p output_topic:="/planning/ml_planner/auto/trajectory"
```

## 実行結果を確認

以下のコマンドで出力が得られていれば、正しく実行できています。

```sh
ros2 topic echo /planning/ml_planner/auto/trajectory
```

## Tips

Sample ROS Nodeで提供している重みファイルは、公道走行を想定したtrajectoryを生成します。詳細は[FAQ](./ml_sample/faq.md)を参照してください。
