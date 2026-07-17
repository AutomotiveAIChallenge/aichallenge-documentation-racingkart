# PilotNet

PilotNet (DAVE-2) では、カメラから出力された画像データを用いて、機械学習モデルによる推論を実行し、制御信号（steering, acceleration）を出力します。

このドキュメントでは、PilotNetの学習方法と実行方法について説明します。

- アルゴリズムの説明: [ml_sample/algorithms.md](algorithms.md#dave-2)
- ROS 推論ノード: [pilot_net_controller](https://github.com/AutomotiveAIChallenge/aichallenge-racingkart/tree/main/aichallenge/workspace/src/aichallenge_submit/pilot_net_controller)
- 入力: フロントカメラ画像 (66x200)
- 学習: PyTorch
- 推論: NumPy
- 入力前処理: 上部 37.5% クロップ → 66x200 リサイズ (抽出時) → YUV 変換 (学習時)

## 事前準備

[環境構築](../setup/introduction.ja.md)を実施して、`make dev` コマンドによってAutowareとAWSIMが使用できることを確認してください。また、[.envの記載](../setup/gpu-simulation.ja.md#env-check)を参考にGPUが使用できていることを確認してください。

## 全体の流れ

以下の手順でPilotNetを使います。提供する重みファイルをそのまま使い、まずは動かしてみたい方はStep1後に直接Step4にお進みください。

- Step1. AWSIMの設定をE2E用にする
- Step2. 学習用データの取得
- Step3. 学習
- Step4. PilotNetを使いAutowareを動かす

## Step1. AWSIMの設定をE2E用にする

[TinyLidarNetの手順](./tiny_lidar_net.md#step1)と同様です。

## Step2. 学習用データの取得

[TinyLidarNetの手順](./tiny_lidar_net.md#step2)と同様です。

## Step3. 学習

rosbag保存するときに使用したターミナルか、新規ターミナルで再度 `make autoware-bash` コマンドを実行してAutoware環境が有効なコンテナに入ります。

以下の1〜5の手順で学習を進めます。各手順の詳細は折りたたみの説明（クリックで展開）にまとめています。実際に実行するコマンドは、説明の後にある一括コマンドを上から順にコピーして進めてください。

??? note "1. rosbagを訓練データと検証データに割り振る"
    ここでは、流れを掴むために訓練データと検証データに取得したデータをそのままコピーしています。実際には、訓練データと検証データを別のものにしたり、データを選定するなどの工夫を行ってください。

    精度を上げたい場合は後述の [train/val 分割と Augmentation](#train-val-augmentation) を参照してください。

??? note "2. rosbagを学習用datasetに変換"
    訓練用と検証用の両方を変換します

    以下のような出力が得られたら成功です。

    ```sh
    [INFO] [PID:99328] Found 1 bags. Starting processing with 1 workers.
    [INFO] [PID:99356] Saved rosbag2_autoware: 413 samples (Total: 0.13s)
    [INFO] [PID:99328] All processing finished in 0.34 seconds.
    ```

    このコマンドは内部で以下を実行します:

    1. rosbag から `/sensing/camera/image_raw` と `/control/command/control_cmd` を時刻同期して取得
    2. 前処理を行い `images.npy` (RGB uint8) として保存
    3. ステアリングと加速度を `steers.npy` / `accelerations.npy` に保存

    YUV への変換はここでは行われません。`images.npy` は RGB のまま保存され、次のステップで `train.py` がデータを読み込む際 (`lib/data.py` の Dataset 内、リサイズ後・正規化前) に `color_space: yuv` 設定に従って変換されます。

??? note "3. 学習"
    学習ログ (TensorBoard) は `logs/` 配下、checkpoint は `checkpoints/` 配下に保存されます。`best_model.pth` が val loss 最良のモデルです。

    各種パラメータは `aichallenge/ml_workspace/pilot_net/config/train.yaml` で調整できます。

    ステアのみ学習したい場合 (アクセル学習が不安定なときに推奨):

    ```sh
    python3 ./train.py train.loss.accel_weight=0.0
    ```

    ただしこの方法では出力次元は 2 のままで、アクセル側は未学習になります。走行時はアクセルが不定にならないよう、[アクセル制御の有効/無効設定](#accel-control) で `control_mode` を `"fixed"` に設定してください。

    なお、CPUで学習を回したい場合や、RTX 50 seriesなどを用いていてCUDAがこの環境に対応していない場合は、以下のようにGPUを無効化して実行してください。

    ```sh
    CUDA_VISIBLE_DEVICES="" python3 ./train.py
    ```

??? note "4. 重みファイルの変換"
    .pthファイルを.npyに変換します。

    以下のような出力が得られれば成功です。

    ```sh
    Loaded checkpoint: checkpoints/best_model.pth
    Saved NumPy weights to: weights/converted_weights.npy
    ```

??? note "5. 重みファイルのデプロイ"
    作成した`converted_weights.npy`を、ROS 2 package内のckptディレクトリにコピーします。

```bash
make autoware-bash

# 以後、コンテナ内部でのコマンド

# 1-a. 訓練データの準備
mkdir -p /aichallenge/ml_workspace/train
cp -r /aichallenge/ml_workspace/rawdata/* /aichallenge/ml_workspace/train

# 1-b. 検証データの準備（本来は訓練データとは分けるべき）
mkdir -p /aichallenge/ml_workspace/val
cp -r /aichallenge/ml_workspace/rawdata/* /aichallenge/ml_workspace/val

cd /aichallenge/ml_workspace/pilot_net

# 2. rosbagを学習用datasetに変換
python3 ./extract_data_from_bag.py \
    --bags-dir /aichallenge/ml_workspace/train/ \
    --outdir ./dataset/train/
python3 ./extract_data_from_bag.py \
    --bags-dir /aichallenge/ml_workspace/val/ \
    --outdir ./dataset/val/

# 3. 学習の実行
python3 ./train.py

# 全Epochが完了するまで待つか、ある程度収束したらctrl-cで終了します

# 4. 重みファイルの変換(.pthから.npyに変換)
python3 ./convert_weight.py \
    --ckpt ./checkpoints/best_model.pth \
    --output ./weights/converted_weights.npy

# 5. 重みファイルのデプロイ
cp ./weights/converted_weights.npy \
    /aichallenge/workspace/src/aichallenge_submit/pilot_net_controller/ckpt/pilotnet_weights.npy
```

## Step4. PilotNetを使いAutowareを動かす

- `aichallenge/workspace/src/aichallenge_submit/aichallenge_submit_launch/launch/reference.launch.xml` の `control_method` を`pilot_net`に変更します。
- その後、いつも通り `make dev` コマンドによって起動すると、 PilotNetによって車両が動き出します。

## PilotNetのTips

### アクセル制御の有効/無効設定 { #accel-control }

`pilot_net_node.param.yaml` の `control_mode` をデフォルトでは `"ai"` にしています。`"fixed"` に変更すると、ステアのみネットワークが推論し、アクセルは `acceleration` パラメータで指定した固定値を使います。

| `control_mode` | アクセル | ステアリング |
|---|---|---|
| `ai` | NN 出力 | NN 出力 |
| `fixed` | `acceleration` パラメータ (固定値) | NN 出力 |

`output_dim=1` で学習した場合 (ステアのみ学習) は自動的に `fixed` 相当の動作になります。

### train/val 分割と Augmentation { #train-val-augmentation }

上述の手順で示したように、`extract_data_from_bag.py` の出力のままでも学習は開始できますが、汎化性能を上げたい場合はAugmentationが有効です。また、本来は訓練用データと検証用データは分けるべきです。

`prepare_data.py` によって、データセットのtrain/val分割と水平反転 Augmentationを行えます。

```sh
# 1. rosbagを同じ場所に配置する
mkdir -p /aichallenge/ml_workspace/all
cp -r /aichallenge/ml_workspace/rawdata/* /aichallenge/ml_workspace/all

cd /aichallenge/ml_workspace/pilot_net

# 2. rosbagを学習用datasetに変換
python3 ./extract_data_from_bag.py \
    --bags-dir /aichallenge/ml_workspace/all/ \
    --outdir ./dataset/all

# 2-x. datasetにAugmentationを行い、train/valに振り分ける
rm -rf ./dataset/train ./dataset/val  # 古いデータセットが残っていたら削除しておく
python3 prepare_data.py --all-dir ./dataset/all
```

### ワンショット実行 (run_pipeline.bash)

extract → prepare → train → convert を一気に実行できます:

```sh
cd /aichallenge/ml_workspace/pilot_net
./run_pipeline.bash /aichallenge/ml_workspace/rawdata/<bag_dir_name>
```

**注意 (破壊的動作):** `run_pipeline.bash` は実行のたびに `dataset/` ディレクトリ全体、および `checkpoints/`・`logs/` ディレクトリを `rm -rf` で削除してから処理を開始します。既存の学習済み checkpoint や過去に抽出した dataset を残したい場合は、事前に別ディレクトリへコピーしておいてください。

**注意 (損失関数):**  `train.py` を直接実行した場合、`output_dim=2` ではデフォルトで `WeightedSmoothL1Loss` が使われますが、`run_pipeline.bash` は内部で常に `+train.loss_type=mse` を付与するため、`output_dim` の値によらず `MSELoss` で学習されます。

引数で解像度・色空間・出力次元・クロップ比率を変更できます:

```sh
./run_pipeline.bash <bag_dir> <image_height> <image_width> <color_space> <output_dim> <crop_top_ratio>
```

例: ステアのみ (output_dim=1):

```sh
./run_pipeline.bash /aichallenge/ml_workspace/train 66 200 yuv 1 0.375
```

### Notes

- **入力解像度を変える場合は学習側 (`run_pipeline.bash` の引数 または `train.yaml`) と推論側 (`pilot_net_node.param.yaml`) を必ず揃えてください。** ずらすと flatten dim 不一致でモデルが読めません。
- 推論性能: 66x200 でも 40Hz は CPU 推論で厳しい場合があります。必要なら ONNX Runtime への移行を検討してください。

## TinyLidarNetとPilotNetで共通のTips

[TinyLidarNetのTips](./tiny_lidar_net.md#tips)を参考にしてください。
