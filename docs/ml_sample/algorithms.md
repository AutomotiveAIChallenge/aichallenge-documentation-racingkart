# Algorithms

教材への理解を深めるために，理解しておくと良いアルゴリズムについて解説します．

## 前提知識

- 機械学習，深層学習の知識
    - MLP, CNN, Transformer等の用語について理解している方を対象とします．

## ALVINN

- 1980年代に発表された，深層学習による自動運転手法です．
- 当時の計算能力は非常に限られていたため，たった3層の全結合型Neural Networkが使われていました．
- 論文: [An Autonomous Land Vehicle In a Neural Network](https://proceedings.neurips.cc/paper/1988/file/812b4ba287f5ee0bc9d43bbf5bbe87fb-Paper.pdf)

![ALVINN](https://jmvidal.cse.sc.edu/talks/ann/alvinn2.gif)

## DAVE-2

- 2016年にNVIDIAから発表された手法で，CNNを用いています．
- ALVINNよりも計算機が強力になったものの，5層のconvolution layerと3層の全結合層からなる，コンパクトな構成でした．
- 論文: [End to End Learning for Self-Driving Cars](https://arxiv.org/abs/1604.07316)

![](https://figures.semanticscholar.org/0e3cc46583217ec81e87045a4f9ae3478a008227/3-Figure2-1.png)

## UniAD

- CVPR2023でOpenDriveLabから発表された手法で，画像を入力とし，trajectory(waypoints)を出力します．現在幅広く使われている，センサが入力，trajectoryが出力となる自動運転手法の基礎となっています．
- "Query based"と呼ばれる方法で，各module間をつなぐ手法を採用．
- 複数の画像を，[BEVFormer](https://arxiv.org/abs/2203.17270)と呼ばれる手法で処理し，BEV特徴量(Bird-eye-view, 鳥瞰図のように交通環境を上から見たときの特徴量)を取得．
- Map情報はRasterで表現しており，かなり推論が遅いです(A100で1~4 FPS)
- 論文: [Planning-oriented Autonomous Driving](https://arxiv.org/abs/2212.10156)
- 学習・推論用code: https://github.com/OpenDriveLab/UniAD

![UniAD](https://opendrivelab.com/assets/publication/uniad.jpg)
![UniAD-poster](https://github.com/OpenDriveLab/UniAD/blob/v2.0/sources/cvpr23_uniad_poster.png?raw=true)

## VAD

- ICCV2023で発表された手法です．BEV特徴量の使用，"Query based"な思想をUniADから引き継ぎながらも，Raster mapではなくVector mapを使用することで高速化・軽量化を達成．RTX3090で16.8 Fpsで動きます．
- 論文: [VAD: Vectorized Scene Representation for Efficient Autonomous Driving](https://arxiv.org/abs/2303.12077)
- 学習・推論用code: https://github.com/hustvl/VAD

![VAD Architecture](https://raw.githubusercontent.com/hustvl/VAD/main/assets/arch.png)

Sample ROS Nodeでは`VAD-tiny`と呼ばれるmodelを使用しています．

<details>
<summary>VAD-tinyの詳細</summary>

### VAD-tinyの詳細

- VAD-tinyのinput
  - 6枚の画像(解像度: 384x640)
  - VADが推論に使う基準座標系から各cameraへの座標変換行列
      - python実装において，nuScenesで学習した際のVADの基準座標系がlidar座標系であることから`lidar2cam`と呼ばれます
  - 車両の自己位置・加速度・速度・角速度・yawの値
    　- 車両のCANを通じて取得する情報であることから`can_bus`と呼ばれます
  - 過去のBEV特徴量を現在のBEV特徴量と結合する際に，過去のBEV特徴量を補正するための情報(`shift`)
      - BEV特徴量のサイズと，`can_bus`に含まれるyawの情報から計算されます

- VAD-tinyのoutput trajectory
    - `[3, 6, 2]`のサイズの配列を出力
        - 3: 右折，左折，直進の3種類
        - 6: 6 step先までのwaypointを推論
        - 2: (x,y)

</details>

<!-- ## DiffusionDrive

## MonAD

## PRIX -->

# VLM based planner

- 言語モデルを使用したPlannerも多数登場しています．いくつか例を紹介します．

### [EMMA](https://waymo.com/research/emma/)

- Geminiを自動運転データでfine-tuningして使用しています．
- 道路上にかばんやはしごが落ちていたら避ける軌道を出力し，路上にりすがいたらslow downするなど，long-tail driving scenario(珍しいシナリオ)に対応できるとの結果が得られています．
- 論文: [EMMA: End-to-End Multimodal Model for Autonomous Driving](https://waymo.com/research/emma/)

### [OmniDrive](https://arxiv.org/abs/2405.01533)

- NVIDIAがCVPR2025で発表した論文
- 「もしこの状況でこうするとどうなりますか？」というcounterfactual reasoning(反実仮想)の訓練ができるようなdatasetを作成し，学習．
- 論文: [OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counterfactual Reasoning](https://arxiv.org/abs/2405.01533)
- 学習・推論用code: https://github.com/NVlabs/OmniDrive

![](https://cvpr.thecvf.com/media/PosterPDFs/CVPR%202025/34693.png?t=1748858551.4455686)

### [S4-Driver](https://arxiv.org/abs/2505.24139)

- WaymoがCVPR2025で発表した論文
- 「VLMが2次元画像でしか事前学習しておらず，Motion Planningでの性能が低い」という課題感から，UniAD, VADのようなBEV特徴量を使った手法から着想を得て，BEV特徴量を使用したVLM modelを提案しています．
- 論文: [S4-Driver: Scalable Self-Supervised Driving Multimodal Large Language Modelwith Spatio-Temporal Visual Representation](https://arxiv.org/abs/2505.24139)

![](https://cvpr.thecvf.com/media/PosterPDFs/CVPR%202025/32619.png?t=1748995327.7679746)

# VLM + BEVのhybrid planner

- UniAD, VADのようなBEV特徴量を用いたPlannerと，VLMとを統合したPlannerも提案されています．

### [DriveVLM](https://arxiv.org/abs/2402.12289)

- `"Fast&Slow"`と呼ばれる，「VLMによる遅い推論」と「VADのようなmodelによる速い推論」を組み合わせたmodel.
- 「草木が落ちているような状況で回避軌道を生成できる」「警察の手でのジェスチャーに対応した軌道を生成できる」といった，long-tail driving scenario(珍しいシナリオ)に対応できるとの結果が得られています．
- 論文: [DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models](https://arxiv.org/abs/2402.12289)
- youtube: https://www.youtube.com/embed/mt-SdHTTZzA

![](https://tsinghua-mars-lab.github.io/DriveVLM/images/pipeline.png)



### [Senna](https://github.com/hustvl/Senna)

- VLMと学習ベースのPlannerを結合した手法です．
- VLMでhigh levelなcommandを決定し，VADのようなBEV特徴量を用いたmodelで使用します．
- 論文: [Senna: Bridging Large Vision-Language Models and End-to-End Autonomous Driving](https://arxiv.org/abs/2410.22313)
- code: https://github.com/hustvl/Senna

![](https://github.com/hustvl/Senna/raw/main/assets/teaser.png)

<!-- # VLA based planner

### [OpenDriveVLA]() -->
