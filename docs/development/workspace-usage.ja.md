# AIチャレンジの進め方

![Where-to-start](./images/where-to-start.drawio.svg)

AIチャレンジではオープンソースソフトウェアを駆使しています。運営から提供されるコードとウェブプラットフォームを利用することで、初期開発フェーズをスキップし、競技のテーマに合わせた開発をすぐに開始できます。
このアプローチには、「車輪の再発明」を避けることができるという大きな利点があります。さらに、誰でも気軽に大会に参加でき、一貫した評価基準で大会を運営できるというメリットもあります。

初めて参加される方々は、先人たちが築き上げた基盤の上に立ち、自動運転に必要な機能がほとんど揃っている状態からスタートします。これからは、コミュニティによる「取り組みの公開」を通じて、競技領域での独自の開発を深めるチャンスです。
さらに、自動運転の理解を深めるために、運営が用意した「[Autoware Practice](../course/index.ja.md)」やROS 2のコミュニティが提供する「[ROS 2](https://docs.ros.org/en/humble/Tutorials.html)」の学習プログラムを活用することをお勧めします。

既にチャレンジに参加された方々には、ご自身の経験を公開し、コミュニティに貢献して大会の発展に寄与していただければと思います。皆さんの積極的な参加が、大会をさらに充実させることに繋がります。

<!-- ※AIチャレンジで開発する上でベースとなるソースコードは[大会用リポジトリ](https://github.com/AutomotiveAIChallenge/aichallenge-2025/tree/main/aichallenge/workspace/src/aichallenge_submit)内で提供されています。 -->

参加者の皆様にはこちらのコードやパラメータをカスタマイズすることで開発を進めていただきますが、Autowareに不慣れな方はまずは[入門講座](../course/index.ja.md)を一通りやっていただくことをお勧めします。

※リポジトリ内のコードを使わず独自に開発する方など、各種仕様について知りたい方は[インターフェース仕様](../specifications/interface.ja.md)、[シミュレータ仕様](../specifications/simulator.ja.md)のページを参照してください。

??? tip "参加者有志の参考記事を読んでみる"
    参加者有志が取り組んでくださった取り組みは[Advent Calendar](https://qiita.com/advent-calendar/2023/jidounten-ai)にまとめられていますので参考にしてみてください。

    どれから読もうか迷った方は2023年度コミュニティ貢献賞を受賞した田中新太さんが記載してくれた[こちらの記事](https://qiita.com/Arata-stu/items/4b03772348dca4f7ef89)から読み進めると良いと思います。

??? tip "パラメータを変更してみる"
    環境構築後何をして良いのかわからない方向けに、まずパラメータを調整してみましょう。
    今回は制御モジュールのsimple_pure_pursuitのパラメータを変更してみることにします。

    `$HOME/aichallenge-racingkart/aichallenge/workspace/src/aichallenge_submit/aichallenge_submit_launch/launch/reference.launch.xml`内の以下の`value`値を調整してみましょう。

    ```xml
    <node pkg="simple_pure_pursuit" exec="simple_pure_pursuit" name="simple_pure_pursuit_node" output="screen">
        <param name="use_external_target_vel" value="true"/>
        <param name="external_target_vel" value="8.0"/>
        <param name="lookahead_gain" value="0.4"/>
        <param name="lookahead_min_distance" value="5.0"/>
        <param name="speed_proportional_gain" value="1.0"/>
    ```

    調整が終わったら再び[ビルド・実行](../setup/build-docker.ja.md)してみましょう。挙動が変わったことが確認できたかと思います。

??? tip "新規パッケージを作成してみる"
    新たに自作パッケージを作成してみましょう。まずはオープンソースのパッケージや[autoware practice](https://github.com/AutomotiveAIChallenge/autoware-practice)をコピーしてみましょう。
    以下のように進めると良いと思います。

    1. 元のパッケージをコピーして、下記を変更
        - パッケージ名
        - フォルダ名
        - コード
        - package.xml
        - CMakeLists.txt
    2. aichallenge_submitの中に配置
    3. aichallenge_submit_launch内のlaunchファイル(reference.launch.xml)を変更

    ※コピー元のパッケージのライセンスを違反しないよう各自確認お願いいたします。

??? tip "[任意]Trajectoryの編集をしてみる"
    2025年度のAIチャレンジでは岐阜大学のチームが作成してくれた[Trajectory Editor](https://github.com/AutomotiveAIChallenge/aichallenge-trajectory-editor)などのツールを使ってTrajectoryの編集をしていきます。

    [Readme](https://github.com/iASL-Gifu/aichallenge-trajectory-editor)にステップバイステップのインストラクションなどがあるので参考にしてみてください。

    作成したlanelet2 mapは`aichallenge/workspace/src/aichallenge_submit/simple_trajectory_generator/data`に格納してください。

??? tip "提出してみる"
    ワークスペースのカスタマイズを行ったら[ここ](../preliminaries/submission.ja.md)を参考に提出をしてみましょう。

## [Next Step:メインモジュールについて知る](./main-module.ja.md)
