# ビルド・実行

大会用リポジトリでは、実際の動作環境はすべてDocker内で完結して提供されています。リポジトリの利用は以下の流れで行います。

1. 大会環境のDockerイメージのビルド
2. Dockerコンテナ上でのAutowareのビルド
3. Dockerコンテナ上でのAutowareとシミュレータの同時起動

## 開発

このリポジトリは、make → `docker compose` で AWSIM と Autoware を動かす、という形になっています。

- **AWSIM**: シミュレータ（`simulator` サービス）
- **Autoware**: 自動運転ソフト（`autoware` サービス）
- **`make`**: `docker compose ...` を叩くための「短い入口」
- **出力先**: だいたい `output/` 配下（ログや結果）

### 開発として起動して触りたい（おすすめ）

```bash
./docker_build.sh dev      # 開発用イメージを作る（最初に1回）
make autoware-build        # ワークスペースをビルド（最初に1回）
make dev                   # AWSIM + Autoware を起動

# 終わったら（困ったらこれ）
make down
```

### 評価フローを最後まで回したい（結果を残したい）

```bash
make eval      # 評価を実行（実行後に自動で停止・片付けまでやる）
```

## コマンド早見表（「何をする？」「いつ使う？」）

| コマンド | 役割 | 使うタイミング | 主な出力 |
| --- | --- | --- | --- |
| `./docker_build.sh dev` | 開発用イメージを作成 | 初回 / Dockerfile更新後 | `output/_host/latest/docker_build.log` |
| `make autoware-build` | ROSワークスペースをビルド | 初回 / 依存・ソース更新後 | 端末出力（必要に応じてログ確認） |
| `make dev` | AWSIM + Autoware を起動（開発用） | 手元でデバッグするとき | `output/<timestamp>/d<domain_id>/autoware.log, etc` |
| `make eval` | 評価を実行して結果を保存 | 評価を回したいとき | `output/<timestamp>/d<domain_id>/autoware.log, etc` |
| `make ps` | 起動中コンテナを確認 | 動作確認したいとき | 端末出力 |
| `make down` | コンテナ停止・片付け | 終了時 / 詰まったとき | 端末出力 |

## 使い分け（迷ったらここ）

- **`make dev`**: 「起動して触る」。止めるまで動き続けます。最後は `make down`。
- **`make eval`**: 「評価を回して結果を残す」。終わったら自動で停止・片付けます（途中で `Ctrl+C` しても後片付けが走ります）。

詳細な運用設定（環境変数）とトラブル時の戻し方は、[開発の参考](./reference.ja.md)を参照してください。

## [Next Step: 開発をしてみる](../development/workspace-usage.ja.md)

以上で環境構築は終了です！次は実際に開発を行ってみましょう。
