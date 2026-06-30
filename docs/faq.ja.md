# FAQ

## 参加について

??? question "GPU未搭載のUbuntuPCでも参加できますか？"
    Intel内蔵GPUでもご参加いただけます。GPUが完全に未搭載PCの場合は、AWSIMをヘッドレスモードで実行することで最低限の動作確認はできます。

??? question "MacやWindowsでも参加できますか？"
    本大会のサポート対象はUbuntu 22.04です。詳細のご案内はできませんが、一般的に下記のような方法があると思われます。なお、性能やパッケージの有無、ホスト-コンテナ内の通信設定などの問題が起きる可能性があります。

    - デュアルブートでUbuntuを用意
    - Windows上にVMでUbuntuを用意 (Hyper-V、VirtualBox、VMwareなど)
    - WSL2上にUbuntuを用意
    - Windows上にdocker環境を用意（直接、Autowareのイメージを入れる）
    - クラウドに環境を構築 (過去の大会ではAWSを利用して参加されている方もいらっしゃいました)

??? question "プログラミング経験はどの程度必要ですか？"
    C++またはPythonの基礎的な知識があれば参加できます。まずはパラメータ調整から始めて、慣れてきたらコードの変更に挑戦してみてください。[基礎演習](./course/index.ja.md)ではゼロからステップバイステップで学べます。

??? question "Autoware / ROS 2 を触ったことがないのですが大丈夫ですか？"
    大丈夫です。多くの参加者がAutowareやROS 2に初めて触れる方です。[開発の進め方](./development/development-guide.ja.md)を参考にまずはコマンドを打つところから始めてみましょう。その後、[基礎演習](./course/index.ja.md)等で学んでいきましょう。

??? question "どのようにしてAutowareを改良して参加すればよいかが分かりません。"
    段階的に以下のアプローチで進めることをお勧めします。

    1. **パラメータ調整**: `reference.launch.xml` の速度やゲイン値を変更する（[開発のアイデア](./development/development-ideas.ja.md)参照）
    2. **基礎演習で学ぶ**: [基礎演習](./course/index.ja.md)で車両制御や経路追従の基礎を習得する
    3. **ノードの改良・置き換え**: [メインモジュール](./development/main-module.ja.md)を参考に、PlanningやControlのノードをカスタマイズする

    また、外部の方の記事ですが、[こちら](https://qiita.com/h_bog/items/86fba5b94b2148c4d9da)も参考になるかもしれません。

??? question "FAQに載っていない質問はどこで聞けますか？"
    [コミュニティページ](./community.ja.md)から参加者同士の情報交換の場にアクセスできます。

    環境構築について質問する場合は、症状に加えてご自身の環境と`./setup.bash doctor`の結果もご共有いただけると、よりスムーズにアドバイスできます。

## 環境構築

??? question "`WARNING unable to detect os for base image 'aichallenge-racingkart-dev', maybe the base image does not exist`が出ます。"
    Dockerイメージのビルドをお願いします。

??? question "Dockerがpullできません"
    `newgrp docker`か`sudo service docker restart`でdockerの再起動またはUbuntuの再起動をお願いします。

??? question "`make dev`で起動しません。"
    以下を確認してください。

    1. GPUドライバが正しくインストールされているか確認: `nvidia-smi`でGPU情報が表示されることを確認してください。
    2. Dockerコンテナが残っていないか確認: `make down` および `make down_all` を実行してから再度`make dev`を試してください。
    3. Dockerイメージがビルド済みか確認: `./docker_build.sh dev`を実行してから再度試してください。

??? question "AWSIMがコアダンプで終了します。"
    AWSIMを起動した直後にcoredumpで終了する場合、GPUのメモリが不足している可能性があります。そのため、`nvidia-smi`でGPUメモリの利用率が限界に達していないか確認してください。
    なお、GPUのメモリは11GB以上を推奨しています。

??? question "AWSIMがピンク画面になります。"
    GPUの認識に失敗している可能性があります。例えば、NVIDIA GPUのみが存在するPCで、`.env` に `docker-compose.gpu.yml` が追加されていないとピンク画面になります。[.envの確認](./setup/gpu-simulation.ja.md#env-check)を参照してください。まずはコンテナ内で `nvidia-smi` が正常に動作することを確認してください。NVIDIAドライバのインストール状況とDockerのGPU設定も確認してください。
    ![Unityピンク画面](https://github.com/user-attachments/assets/2e9b5b06-18a3-476d-bf32-4b17d78f322e)

??? question "AWSIMが重いです。（Intel 内蔵 GPU 使用時）"
    ご使用のGPUのスペックをご確認ください。特にPC全体が重くなってしまう場合はスペックが足りていない可能性があります。例えば第10世代 Intel Coreの内蔵GPUだと、3FPS程度しか出ませんでした。

??? question "AWSIMが重い・たまに固まります。（NVIDIA GPU 使用時）"
    NVIDIA GPU と Intel 内蔵 GPU の両方が搭載されたPCを使用している場合は、NVIDIAを優先して使用するように設定してください。

    ```bash
    sudo prime-select nvidia
    ```

??? question "AWSIMの起動・終了に時間がかかります。"
    現状、数秒〜10秒程度かかります。

??? question "AWSIMが黒画面のままになることがあります。"
    稀に起動に失敗することがあります。 `make down_all` で全コンテナを終了してから再度起動してください。100%の頻度で黒画面になる場合は設定・環境の問題であるため、セットアップ手順を再確認してください。

??? question "AWSで環境構築したところ、AWSIMは表示されたが、Rvizがブラックスクリーンとなりました。"
    `sudo apt upgrade`で治ったという事例がありますので、内容を確認の上、お試しください。
    また、[過去Issue](https://github.com/ros2/rviz/issues/948)にてご質問内容と似た質問がありましたので、こちらも合わせてご確認ください。

## 開発・デバッグ

??? question "pythonでパッケージを作成すると実行時 no module named * のerrorが起きます。"
    [こちら](https://zenn.dev/tasada038/articles/5d8ba66aa34b85#setup.py%E3%81%ABsubmodules%E3%81%A8%E3%81%97%E3%81%A6%E3%83%91%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B8%E3%82%92%E8%BF%BD%E5%8A%A0%E3%81%99%E3%82%8B)を参考にしてみてください。

??? question "ros2 topic list が表示されません。"
    コマンドをDockerコンテナ内で発行していることと、`ROS_DOMAIN_ID`が設定されていることを確認してください。例えば、　`export ROS_DOMAIN_ID=1`

    もしもDockerコンテナ外で確認している場合は、ワークスペースがソースされていることの確認をお願いします。

??? question "トピックの型を調べるには、どのようなコマンドを打てばよろしいでしょうか。"
    topicの型を調べる際は`ros2 topic info -v fuga_topic`もしくはnodeが特定できれば、`ros2 node info hoge-node`で調べることができます。
    その他にもROSに関する情報を調べたい場合は「ROS2　コマンド」で、ネット検索すると良いかもしれません。

??? question "Rviz上で地図・ルートが表示されません。"
    使用しているマップデータが適切な場所に配置されいるか・正しいかを確認してください。

??? question "`docker_run.sh: 行 35: rocker: コマンドが見つかりません`が出ます。"
    現在の推奨ワークフローでは`make dev`を使用するため、通常は`docker_run.sh`を使う必要はありません。[開発の進め方](development/development-guide.ja.md)を参照してください。デバッグ目的で`docker_run.sh`を使用する場合は、[rockerの公式README](https://github.com/osrf/rocker?tab=readme-ov-file#debians-recommended)に従ってインストールしてください。

??? question "Rockerが起動しません。"
    まず、rockerがインストールされているかの確認をお願いします。
    インストールされているにも関わらず、起動しない場合は権限をご確認ください。過去の事例ですと、イメージをビルドしたアカウントと実行する際のアカウントの種類・権限が異なると実行できないことが報告されています。

## Autoware

??? question "制御モードを変更するにはどうすればいいですか？"
    `reference.launch.xml`の`control_mode`引数を変更することで制御モードを切り替えられます。

    - `mpc`（デフォルト）：MPCベースの制御
    - `pure_pursuit`: Pure Pursuitベースの制御
    - `tiny_lidar_net`: TinyLiDARNetによるEnd-to-End制御
    - `pilot_net`: PilotNetによるEnd-to-End制御
    - `joycon`: 手動テレオペ操作

??? question "経路生成（Behavior Path/Motion Planner）に関して教えてください。"
    behavior plannerは、主にODD3以上のいわゆる一般道での走行を行うのに必要な機能（一時停止線、横断歩道、信号停止）など破ってはいけない交通ルールを加味したplanningを行うものとなっています。
    それ故、回避機能もルールベースの回避で最適化を行っていません。
    一方でmotionはODD2以下のいわゆる限定区域や限定空間での走行を実現するもので、例えば信号や、地図の情報等といった情報を扱うものはありません。
    障害物の回避や、停止、速度の最適化など、通常走行に必要な機能を担うものとなっています。

??? question "Autowareの回避行動について教えて下さい"
    回避には二種類あり、behavior pathとobstacle avoidanceがあります。
    デフォルトではobstacle avoidabceの回避はoffで、経路の平滑化のみ行われる設定になっています。
    また、デフォルトではbehavior pathで回避する設定にはなっていますがその際の回避対象物は車とトラックのみです。

??? question "center pointについて教えて下さい。"
    center pointは車両とトラックと歩行者を検知してくれますが、ダンボールなどタグ付けされていないものは検知できません。
    ただ、現状のautowareとしてはplanningがobjectを受け取らないと動かないようになっており、objectを受け取る段階でcenter pointを使うデフォルトの構成にしていると、以下の2つの原因により不具合が起こります。

    1. center pointが死んだときにplanningが経路を生成できなくなる
    2. data associationでclusteringによる障害物検知結果が消される

    そのため、perceptionの構成はautoware miniが理想的ですが、このあたりを理解してノードの足し引き、取捨選択をして実装することははなかなか難しいため、center pointが問題なく動くようにすることは重要になってくるかもしれません。
    [参考](https://autowarefoundation.github.io/autoware.universe/main/perception/autoware_lidar_centerpoint/)

??? question "mpcのチューニングをしたいのですが，今回AWSIMで使用されているモデルパラメータ（遅れや時定数など）は公開されていないでしょうか．"
    遅れや時定数については計測も公開もされていませんが、基本的な仕様については[こちら](./specifications/simulator.ja.md)に公開されています。

??? question "ドメインIDとは何ですか？"
    本大会ではマルチ車両対応のため、ROS 2のドメインID機能を使用しています。

    - **ドメイン0**: AWSIM（シミュレータ）が使用
    - **ドメイン1〜4**: 各車両が使用

    `domain_bridge`ノードがドメイン間のトピックを橋渡しします。通常の開発では、ドメインIDを意識する必要はありません。

## シミュレータ・実行

??? question "車を初期位置にリセットするにはどうすればいいでしょうか。"
    AWSIMのキーボード操作で`Space`キーを押すとリセットできます。また、`/admin/awsim/reset`トピックに`std_msgs/msg/Empty`をPublishすることでもリセットが可能です。

??? question "AWSIMの動作が安定しません。"
    GPUの性能不足が原因の一つになります。
    高性能GPUの利用が難しい場合は、awsimの画面の下部にスライドバーでtime scaleを0.5くらいに設定すると安定して動作する可能性があります。

??? question "センサの追加取り付けは可能ですか。"
    同一条件・難易度で課題に取り組んでいただくために、新たなセンサの取り付けは不可としています。

## 解決しない場合

[:material-arrow-right-circle: コミュニティで情報を探す](./community.ja.md){ .md-button .md-button--primary }
