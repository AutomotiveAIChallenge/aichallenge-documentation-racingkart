# 提出手順（SW部門 SIM予選）

## オンライン環境

Sim to Real SW部門 SIM予選では、シミュレーターと自動採点機能を備えたオンライン環境を使用して採点が行われます。以下の手順に従って、作成したパッケージ群をオンライン環境にアップロードしてください。アップロード後、シミュレーションが自動で開始され、結果が表示されます。

※本ページのスクリーンショットは2025のものです

## 提出手順

オンライン環境への提出は以下の手順で行います。

1. ソースコードの圧縮

    - `./create_submit_file.bash`を実行してaichallenge_submitディレクトリを圧縮します。
    - 圧縮したファイルはaichallenge-racingkart/submit/aichallenge_submit.tar.gzに保存されています。

2. ローカル評価環境での動作確認

    詳細は[開発の進め方 — ローカル評価の手順](../development/development-guide.ja.md#ローカル評価の手順)を参照してください。

3. オンライン採点環境への提出

    [オンライン環境](https://aichallenge-board.jsae.or.jp)にアクセスします。
    <img src="./images/topImage.png" width="100%">

    右上の「Login」 ボタンからログインします。
    <img src="./images/siteImage1.png" width="100%">

    ログインが完了したら「Submit Code」ボタンから`aichallenge_submit.tar.gz`をアップロードしてください。アップロード後、ソースコードのビルドとシミュレーションが順に実施されます。
    <img src="./images/siteImage2.png" width="100%">

    正常に終了した場合、「Success」と表示されます。
    ビルドに失敗したり、launchに失敗した等でスコアが出力されていない場合は「Failed」と表示されます。この場合、サーバーサイドでの内部エラーの可能性があるため、再アップロードをお願いします。問題が続く場合はslackでお問い合わせください。

    <img src="./images/siteImage3.png" width="100%">


## 結果の確認手順

- オンライン環境での走行が終わると、最新の順位を確認できます。
- ラップタイムやログなどの走行時の詳細データを提出履歴の右端のボタンから確認することができます。
    - `result-summary.json`、rosbag、`autoware.log`を確認することができます。

    <img src="./images/siteImage4.png" width="100%">

    <img src="./images/siteImage5.png" width="100%">

## Failedの場合

- packageの依存関係に問題がないか確認

    - 使用言語に応じて、`package.xml`、`setup.py`、または`CMakeLists.txt`に依存関係の漏れがないか確認してください。

- dockerの確認

    - 以下のコマンドでDocker内を確認し、必要なディレクトリに正しくインストール・ビルドされているか確認してください。

    - `docker run -it aichallenge-racingkart-eval:latest /bin/bash`

- 確認するディレクトリ:

    - `/aichallenge/workspace/*`
    - `/autoware/install/*`
