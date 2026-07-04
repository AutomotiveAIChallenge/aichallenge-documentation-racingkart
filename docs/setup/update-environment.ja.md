# 環境のアップデート

大会環境の重大なアップデートがあった際には適宜アナウンスがあります。都度必要な手順も併せてアナウンス予定ですが、参考までにこちらに記載します。

!!! warning "シミュレータのアップデート"
    使用するシミュレータ「AWSIM」は、大会期間中に複数回の更新を予定しています。

    アップデートの実施については告知いたしますが、アップデート内容については課題の難易度に関わるため告知いたしません。参加者の皆様には、ご自身でアップデート内容を調査していただくことを想定しています。

## 全てをまとめて更新する場合

```bash
./setup.bash bootstrap
# 各種確認にy応答
```

## Dockerの更新

下記コマンド実行後、Dockerイメージの再ビルド、Autowareの再ビルドが必要になります。

```bash
./setup.bash pull image
# または
docker pull ghcr.io/automotiveaichallenge/autoware-universe:humble-latest
```

## Autowareの更新

下記コマンド実行後、Dockerイメージの再ビルド、Autowareの再ビルドが必要になります。

```bash
cd aichallenge-racingkart # path to aichallenge
git pull origin/main
```

## AWSIMの更新

```bash
./setup.bash download awsim
```
