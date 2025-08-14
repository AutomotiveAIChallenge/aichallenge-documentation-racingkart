# Getting started: VLM Plannerの実行

このドキュメントでは、Gemini APIとAWSIMを用いて、VLM Plannerを動かす方法について説明します。

## VLM Plannerの実行

- [VLM Planner環境側の準備](./getting_started_vlm_setup.md#vlm-planner環境側の準備)で作成したdocker container内で、以下を実行しましょう。
  - 以下のコマンドを実行し、VLM Plannerを動かしてみてください。

```sh
# Run the VLM planner node with custom output topic
cd /home/e2e-utils-beta/src/vlm_planner
python vlm_planner_node.py --ros-args -p output_topic:="/planning/ml_planner/auto/trajectory"
```

## AWSIMの実行

- [AWSIM側の準備](./getting_started_vlm_setup.md#awsim側の準備)にて作成したdocker container内で、`./run_evaluation.bash`を実行しましょう。
  - scaleは0.20程度に変更しましょう。(Geminiが5秒に1回しか推論できないため。)

![camera_awsim_after](../assets/camera_awsim_after.png)

## 実行結果を確認

以下のコマンドで出力が得られていれば、正しく実行できています。

```sh
ros2 topic echo /planning/ml_planner/auto/trajectory
```

## Tips

このSampleでは、`gemini-2.5-flash-lite`をそのまま使用しており、サーキット用のチューニングができておらず、ヘアピンを回ることができない状態となっています。以下のTipsを参考に、改善にトライしてみてください。

- [`e2e-utils-beta/src/vlm_planner/vlm_planner.py`](https://github.com/AutomotiveAIChallenge/e2e-utils-beta/blob/7dc5cf2515d7fa8cecfee5b34b8474e8f7c170f1/src/vlm_planner/vlm_planner.py#L47)を更新することでモデルを変更できます
    - デフォルトでは`gemini-2.5-flash-lite`が使用されています。

```python
self.model = genai.GenerativeModel("gemini-2.5-flash-lite")
```

- プロンプト([`e2e-utils-beta/src/vlm_planner/prompt.py`](https://github.com/AutomotiveAIChallenge/e2e-utils-beta/blob/main/src/vlm_planner/prompt.py))を更新することでも改善ができる可能性があります。

- [Vertex AIでのファインチューニング](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-use-supervised-tuning?hl=ja)が軌道の改善に役立つ可能性があります。
