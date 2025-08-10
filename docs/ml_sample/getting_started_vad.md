# Getting started

## AWSIM側の準備

[環境構築](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/requirements.html)のドキュメントに従い，[描画ありAWSIMの起動](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/requirements.html)と[大会用リポジトリのビルド・実行](https://automotiveaichallenge.github.io/aichallenge-documentation-2025/setup/build-docker.html)までを実施してください．

```sh
cd ~/aichallenge-2025
./docker_run.sh dev gpu
```

```sh
cd /aichallenge
./build_autoware.bash
./run_evaluation.bash
```


AWSIMが表示されたら，AWSIMでuse imageのボタンを押してカメラ画像を有効にします．

![alt text](../assets/camera_awsim.png)

## local環境側の準備

!!! info

    この手順書に従って環境構築を行うことで，local環境のCUDA, TensorRT環境が変更されます．
    local環境のCUDA関連の設定が変更されることで，PCが正常に立ち上がらない，ログインループなどの症状が発生することがあります．

### sample model(onnx)のdownload

- nuScenes datasetで学習されたonnx fileをdownloadします
  - `$HOME/autoware_data/vad`というディレクトリを作成し，onnx fileをその中に格納してください．

### docker run

```sh
rocker \
  --nvidia \
  --x11 \
  --network host \
  --user \
  --rmw fastrtps \
  --volume /home/shintarotomie/tmp/e2e_utils_beta:/home/e2e_utils_beta \
  --volume ~/autoware_data:/home/autoware_data \
  --name aichallenge-e2e-utils \
  ghcr.io/autowarefoundation/autoware:universe-devel-cuda \
  /bin/bash
```



## TODO

- TODO(Shin-kyoto): コードベース側を整備し，以下の2つの手順を書き上げる．
　- VLM plannerを用いた走行
  - VAD ROS Node + VLM selectorを用いた走行
