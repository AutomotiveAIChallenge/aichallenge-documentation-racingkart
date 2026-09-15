# 03. 障害物回避

安全な自動運転を行うために、障害物を認識し必要に応じて回避する必要があります。ここでは図のように、障害物を認識して回避しながら目標地点に到達することを目指します。

![障害物回避の概念図。車両からゴールまでの経路上に2つの障害物が配置され、車両がそれらを避けながら曲線を描いてゴールへ到達する様子](images/3-1/avoidance_planning.png)

## 03-01. lidarから点群を取得し障害物検知をする

自動運転車両では、障害物を認識するために様々なセンサーが使用されます。代表的なセンサーには以下のものがあります：

1. **LiDAR（Light Detection and Ranging）**:
    - レーザー光を発射し、物体に当たって戻ってくるまでの時間を測定することで距離を計測します。
    - 高精度な3D点群データを生成し、周囲の環境を詳細に把握できます。
2. **カメラ**:
    - 光学センサーを使用して画像を取得します。
    - 画像を用いて物体認識、車線検出、交通標識認識などを行います。
3. **レーダー（Radio Detection and Ranging）**:
    - 電波を発射し、反射して戻ってくるまでの時間を測定します。
    - 長距離の障害物検出に優れ、悪天候でも安定した性能を発揮します。
4. **超音波センサー**:
    - 超音波を発射し、反射して戻ってくるまでの時間を測定します。
    - 近距離の障害物検出に適しており、駐車支援システムなどに利用されます。

今回、lidarを用いた障害物検知を扱うために簡易lidarシミュレータを作成しました。

実際のlidarは観測物体の裏側まで見ることはできませんが、
この簡易lidarシミュレータは物体の輪郭を点群化し、車両の一定範囲内の点群を取得します。

`src/autoware_practice_lidar_simulator/config/object_centers.csv`で座標を指定することで自由に障害物を設定することができます。
3つの障害物を配置するために、以下のようにobejct_centers.csvを編集します。

```diff
+  x_center,y_center
+  7.0,0.0
+  10.0,5.0
+  5.0,-3.0
```

以下のコマンドでシミュレータを起動し、一定範囲内にある障害物の点群が表示されるか確認しましょう。

```bash
ros2 launch autoware_practice_launch practice.launch.xml
```

![RVizの画面。車両の前方に配置された障害物の輪郭に沿って点群（PointCloud）が表示されている様子](images/3-1/simple_lidar_sim1.png)

以下のコマンドを別々のターミナルで実行して、車両の位置が変化するのに伴って取得できる点群が変化するのを確認しましょう。

```bash
ros2 run autoware_practice_course trajectory_loader --ros-args -p path_file:=src/autoware_practice_course/config/trajectory_zigzag.csv
```

```bash
ros2 run autoware_practice_course trajectory_follower --ros-args -p kp:=5.0 -p lookahead_distance:=5.0
```

![RVizの画面。車両が移動したことで検出される障害物の点群の見え方が先の画像から変化している様子](images/3-1/simple_lidar_sim2.png)

## 03-02. 点群情報に基づいて経路・軌道計画し車両を追従させる

取得した点群を元に障害物を回避することを考えます。
障害物を回避するには様々なものがありますが、今回はstate lattice plannerについて説明し実装します。

### State Lattice Planner のアルゴリズム

State lattice plannerとは、車両の現在の状態と目標状態の間に一連の軌道候補を生成し、それぞれの軌道を評価して最適な経路を選択するアルゴリズムです。
以下の画像に軌道を生成するフローを示します。

<div align="center">
  <img src="./images/3-2/flow.jpg" alt="state lattice plannerのフロー図。「目標状態を複数サンプリング」の後に「各目標状態に対して軌道生成」と「コストマップを生成」が並行し、両者を統合して「コストマップを用いて各軌道を評価」する4段階の流れ">
  <br>
  <em>state lattice plannerのフロー</em>
</div>

#### 1. 目標状態をサンプリング

車両の現在の状態からゴールまでの経路上に複数の目標状態をサンプリングします。
今回は予め分かっているゴールまでの軌道に垂直に等間隔に並ぶように目標状態をサンプリングします。

<div align="center">
  <img src="./images/3-2/target_state_sampling.jpg" alt="ゴールまでの軌道上のウェイポイントに垂直な方向に複数の目標状態（青い点）をサンプリングする様子を示す図">
  <br>
  <em>目標状態を複数サンプリング</em>
</div>

#### 2. 各目標状態に対して軌道生成

現在の状態から各目標状態への軌道を生成します。
今回はベジエ曲線を用いて軌道を生成します。

<div align="center">
  <img src="./images/3-2/generate_trajectory.jpg" alt="車両の現在位置からサンプリングされた各目標状態（青い点）へ向けてベジエ曲線状の軌道が複数生成されている様子">
  <br>
  <em>現在の状態から各目標状態への軌道を生成</em>
</div>

#### 3. コストマップを生成

取得した点群データから周囲の障害物情報を反映したコストマップを生成します。コストマップは、各セルに通行の難易度を示す値を持ちます。
今回は点群が存在するセルのコストは100を設定し、点群が存在するセルに隣接するセルのコストは50を設定しました。
また障害物がない場合、予め予め分かっているゴールまでの軌道に戻るようにするために、ゴールまでの軌道のウェイポイントが存在するセルのコストを-1に設定しました。
上記のルールに基づいて各セルのコストを計算します。

例）ゴールまでの軌道のウェイポイントと点群が存在するセルのコストは、-1+100で99となります。

<div align="center">
  <img src="./images/3-2/generate_costmap.jpg" alt="コストマップの図。中心の障害物（ピンク）が最もコスト高で、それを囲む赤い領域がコストが高い領域、外側の緑がコストが低い領域を表す">
  <br>
  <em>コストマップの生成</em>
</div>

#### 4. コストマップを用いて各軌道を評価

各軌道のウェイポイントが存在するセルのコストの総和を軌道のコストとし、最もコストが低い軌道を選択します。

<div align="center">
  <img src="./images/3-2/evaluate_trajectory.jpg" alt="2つの障害物のコスト領域（赤）を避けて中央を通る、最もコストが低い軌道（太い赤線）が選択されている様子">
  <br>
  <em>コストマップを用いて各軌道を評価</em>
</div>

今回は以下のようにtrajectory_plannerノードにstate lattice plannerを作成しました。

![ノード図。simulatorの点群がlidar_driverとobject_segmentationを経てtrajectory_plannerに入力され、trajectory_loaderの軌道と合わせて軌道を生成し、trajectory_followerを介して制御指令をsimulatorへ返す。今回作成するtrajectory_plannerが赤枠で強調されている](images/3-2/nodemap.jpg)

`src/autoware_practice_lidar_simulator/config/object_centers.csv`を修正して障害物の位置を変更します。

```diff
x_center,y_center
-  7.0,0.0
-  10.0,5.0
-  5.0,-3.0
+  47.0,-1.0
+  30.0,1.0
+  15.0,-1.0
```

以下のコマンドを別々のターミナルで実行して画像のように障害物を適切に回避できるか確かめましょう。

```bash
ros2 launch autoware_practice_launch practice.launch.xml
```

```bash
ros2 run autoware_practice_course trajectory_loader --ros-args -p path_file:=src/autoware_practice_course/config/trajectory.csv --remap /planning/scenario_planning/trajectory:=/planning/trajectory_loader/trajectory
```

```bash
ros2 run autoware_practice_course trajectory_follower --ros-args -p kp:=5.0 -p lookahead_distance:=5.0
```

```bash
ros2 run autoware_practice_course trajectory_planner --ros-args -p state_num:=9 -p target_interval:=1.0
```

`state_num`は経路上にサンプリングする目標状態の数、`target_interval`はサンプリングする目標位置の間隔です。
trajectory_plannerを起動する際に他のパラメータも指定できるので是非変更してみてください。ノード起動時に設定できるパラメータは`src/autoware_practice_course/src/avoidance/trajectory_planner.cpp`で確認することができます。

![RVizの画面。車両が障害物のコストマップ（赤い領域）を避けて点群のない側を通過している様子](images/3-2/rviz_image.png)

参考:
[State Lattice Plannerの概要とPythonサンプルコード](https://myenigma.hatenablog.com/entry/2017/07/21/115833)
