# 環境のアップデート

大会環境の重大なアップデートがあった際には適宜アナウンスがあります。都度必要な手順も併せてアナウンス予定ですが、参考までにこちらに記載します。

## Dockerの更新

```bash
./setup.bash pull image
# または
docker pull ghcr.io/automotiveaichallenge/autoware-universe:humble-latest
```

## Autowareの更新

```bash
cd aichallenge-racingkart # path to aichallenge
git pull origin/main
```

## AWSIMの更新

```bash
./setup.bash download awsim
```

??? note "手動でダウンロードする場合"
    One DriveからSimPracticeFor2026内の `AWSIM.zip` をダウンロードし、`aichallenge-racingkart/aichallenge/simulator` に展開します。

    [:material-launch: AWSIMの練習ファイルのダウンロード](https://tier4inc-my.sharepoint.com/:f:/g/personal/taiki_tanaka_tier4_jp/IgCivzVKr4HDSbS1BpXObYmGASNQ6uv7iVjKc6ysyBMernE){ .md-button .md-button--primary  target="_blank" }

    ※現在は大会期間外のため、練習用のファイルのみを提供しています。大会用のファイルは変更される可能性がありますのでご了承ください。

    実行ファイルが`aichallenge-racingkart/aichallenge/simulator/AWSIM/AWSIM.x86_64`に存在していることを確認してください。

    パーミッションを図のように変更します。

    ![パーミッション変更の様子](./images/awsim-permmision.png)
