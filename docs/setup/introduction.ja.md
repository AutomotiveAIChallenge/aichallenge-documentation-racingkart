# 環境構築の流れ

この章では、自動運転 AI チャレンジ 2026（Racing Kart）の開発・実行環境を構築する手順を説明します。推奨環境の確認、ワークスペース準備、Docker と AWSIMの起動までを扱います。

??? info "2025年度参加者向けの変更点"
      - プロセス管理に不向きな `rocker` は、公式手順から除外し、docker composeを活用しました。
      - 個別セットアップ手順を廃止し、一括インストール手順に統一しました。

## 環境構築

curlのパッケージをinstallしましょう。

```bash
sudo apt update
sudo apt install curl
```

次に環境からシミュレーターの実行テストまでを一気通貫で行うコマンドを叩きます。

```bash
curl -fsSL "https://raw.githubusercontent.com/AutomotiveAIChallenge/aichallenge-racingkart/main/setup.bash" | bash
```

## 画面の見方

- `Select branch [default: main]:` が出たら `main` を選択（`Enter`でも可）
- `[y/N]` は各処理を実行するかの確認（基本は `y`）
- `Starting execution...` が表示されたら自動実行開始
- `To stop: make down` が出たら起動確認完了

```.bash
[setup] ℹ️ Bootstrap mode (fresh host)
[setup] Available branches (remote):
[setup]   1) dev
[setup] Select branch [default: main]: main
[setup] ℹ️ Planned steps (answer y/N for each, then execution starts):
[setup]   1) Install base packages (apt)
[setup]   2) Install Docker (if missing)
[setup]   3) Add user to docker group (recommended)
[setup]   4) Clone/update repository (branch=main) -> $USER/aichallenge-racingkart
[setup]   5) Repo preflight: ./setup.bash doctor (requires repo)
[setup]   6) Pull Autoware base image (requires repo)
[setup]   7) Download AWSIM.zip and extract (requires repo)
[setup]   8) Build dev image: ./docker_build.sh dev (requires repo)
[setup]   9) make autoware-build (requires repo)
[setup]  10) make dev DOMAIN_ID=1 (requires repo)
```

以下の10ステップを自動実行します。
途中で `[y/N]` の確認が出たら、通常は `y` を入力してください。

  | ステップ | 内容 |
   |---|---|
  | 1 | :material-package: 必要パッケージを install |
  | 2 | :material-docker: Docker を install |
  | 3 | :material-security: Docker 利用可能化 |
  | 4 | :material-account-group: Docker グループ登録 |
  | 5 | :material-folder-open: リポジトリ準備 |
  | 6 | :material-cloud-download: Autoware イメージ取得 |
  | 7 | :material-download: AWSIM データ取得/展開 |
  | 8 | :material-hammer: 開発用イメージ作成 |
  | 9 | :material-book-education: ワークスペースビルド |
  | 10 | :material-power: AWSIM + Autoware 起動 → `make down` で停止確認 |

それぞれのパッケージをinstallして良いかどうかの同意を求められますので、問題無ければyを入力しましょう。

```.bash
[setup] Install base packages (apt) [y/N]: y
[setup] Install Docker (if missing) [y/N]: y
[setup] Add user to docker group (recommended) [y/N]: y
[setup] Clone/update repository (branch=main) -> $USER/aichallenge-racingkart/aichallenge-racingkart [y/N]: y
[setup] Run repo preflight: ./setup.bash doctor [y/N]: y
[setup] Pull Autoware base image [y/N]: y
[setup] Download AWSIM.zip and extract [y/N]: y
[setup] Build dev image: ./docker_build.sh dev [y/N]: y
[setup] Run make autoware-build (this can take a while) [y/N]: y
[setup] Run make dev DOMAIN_ID=1 [y/N]: y
[setup] ℹ️ Starting execution...
[setup] ℹ️ Running: Install base packages (apt)
```

ここから先は5分程度待つだけです。コーヒーでも入れながら待ちましょう。

:coffee:

セットアップが終わると下記のようなコマンドがでてきてAWSIMとAutowareが勝手に立ち上がります。

```bash
Start dev simulation (AWSIM + Autoware, DOMAIN_ID=1)
make[1]: ディレクトリ '$USER/aichallenge-racingkart' に入ります
Start AWSIM
SIM_MODE=dev docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d simulator
[+] up 1/1
make[1]: ディレクトリ '$USER/aichallenge-racingkart/aichallenge-racingkart' から出ます         0.5s
make[1]: ディレクトリ '$USER/aichallenge-racingkart/aichallenge-racingkart' に入ります
Start Autoware for AWSIM
RUN_MODE=awsim DOMAIN_ID=1 docker compose -f docker-compose.yml -f docker-compose.gpu.yml up -d autoware
[+] up 1/1
 ✔ Container aichallenge-2026-autoware-1 Created                           0.2s
make[1]: ディレクトリ '$USER/aichallenge-racingkart/aichallenge-racingkart' から出ます
To stop: make down  (docker compose down --remove-orphans)
```

AWSIMとAutowareが勝手に立ち上がりました。
![autoware-awsim](./images/autoware-awsim.png)
停止する場合はmake downで停止してください。

以上で環境構築と動作確認が終了しました。

GPU環境がある方はcloneした環境でGPU環境用のNVIDIA Driverのinstall手順も表示していますので、試してみてください。

[Docker環境でGPUをつかう](./visible-simulation.ja.md)

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

---

## コマンド早見表（「何をする？」「いつ使う？」）

| コマンド | 役割 | 使うタイミング | 主な出力 |
| --- | --- | --- | --- |
| `./docker_build.sh dev` | 開発用イメージを作成 | 初回 / Dockerfile更新後 | `output/_host/latest/docker_build.log` |
| `make autoware-build` | ROSワークスペースをビルド | 初回 / 依存・ソース更新後 | 端末出力（必要に応じてログ確認） |
| `make dev` | AWSIM + Autoware を起動（開発用） | 手元でデバッグするとき | `output/<timestamp>/d<domain_id>/autoware.log, etc` |
| `make eval` | 評価を実行して結果を保存 | 評価を回したいとき | `output/<timestamp>/d<domain_id>/autoware.log, etc` |
| `make ps` | 起動中コンテナを確認 | 動作確認したいとき | 端末出力 |
| `make down` | コンテナ停止・片付け | 終了時 / 詰まったとき | 端末出力 |

---

## 使い分け（迷ったらここ）

- **`make dev`**: 「起動して触る」。止めるまで動き続けます。最後は `make down`。
- **`make eval`**: 「評価を回して結果を残す」。終わったら自動で停止・片付けます（途中で `Ctrl+C` しても後片付けが走ります）。

---

詳細な運用設定（環境変数）とトラブル時の戻し方は、[開発の参考](./reference.ja.md)を参照してください。
