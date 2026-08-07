# End to End部門 説明

!!! warning "WIP"
    一部ルールはまだ未定であり、今後更新される可能性があります。

## End to End部門概要

End to End AI部門では予選から決勝まで以下のように進みます。

| 項目 | 日程 | 内容 | 参加チーム |
| --- | --- | --- | --- |
| End to End部門 予選 | 7月1日〜9月1日 | プレゼン書類と走行動画を提出。（[提出フォーム](https://forms.office.com/pages/responsepage.aspx?id=NVLCok7DvEuOMQxVDG-yrJTP427xWZBKkcBQTu6n-vxUMTU5SkpIRFQ3UDRWUk9WNTBLVjUwR0lUNy4u&route=shorturl)） | 参加希望者 |
| SIM決勝準備 | 9月18日 | SIM決勝当日と同じ環境で動作確認・練習走行を行います | 決勝進出チームのうち、参加を希望するチーム |
| End to End部門 SIM決勝 | 9月19日 | 決勝会場のシミュレーション環境で走行 | E2E AI予選の上位16チーム |

!!! warning
    - End to End部門参加チームは、Sim to Real部門への参加も必須となります。
    - End to End部門では、実車両での走行はありません。

## End to End部門の共通ルール

### 走行方式

- AWSIM上でシティサーキット東京ベイ（CCTB）コースを模した環境を走行します。

### 速度とペナルティ

[Sim to Real部門](./sw-class.ja.md)と同様です。

### 使用可能なセンサー

- Camera
- LiDAR
- Steer Angle
- Wheel Odometry
- Gear Status

!!! warning "使用可能なセンサーについて"
    End to End AIの取り組みが重視されるため、GNSS など Sim to Real部門で使えていたセンサーは使用できません。

### 安全ゲート

[Sim to Real部門](./sw-class.ja.md)と同様です。

### 禁止事項

[Sim to Real部門](./sw-class.ja.md)と同様です。

## End to End部門 SIM予選

- End to End部門の予選では、参加チームの取り組みを審査します。
- プレゼン書類と走行動画を提出していただき、審査員による採点を行います。
- [提出フォーム](https://forms.office.com/pages/responsepage.aspx?id=NVLCok7DvEuOMQxVDG-yrJTP427xWZBKkcBQTu6n-vxUMTU5SkpIRFQ3UDRWUk9WNTBLVjUwR0lUNy4u&route=shorturl)

![e2e_submit](./images/e2e_submit.png)

## End to End部門 SIM決勝 { #semifinal }

### 順位決定方式

- 走行は4台同時のレース方式で行われます。周回数は6周です。
- 選抜戦
    - 一般・学生混在で4試合行います。
    - 走行開始位置は、予選での審査結果によって決まります。
    - 書類審査・プレゼン・走行結果の総合点で決勝戦に進出する4チームが選ばれます。
        - 走行結果が上位でも決勝に進めるとは限りません。
- 決勝戦
    - 選抜戦から進出した4チームで試合を行います。
    - 走行開始位置は、選抜戦での順位によって決まります。
    - レースの完走順によって、最終的な順位が決まります。

![e2e_tournament](./images/e2e_sim_tournament.png)

### ルール

- 基本的なルールは上述の共通ルールに従います。
- 走行開始時刻になったら強制的に走行を開始します。セットアップが未完了のチームは、途中からの参加を目指して作業を続けるか、リタイアとなります。
- クラッシュ等で車両がスタックしたり、車両が予期せぬ挙動をした場合、運営側のサポートによる復帰は行いません。
- 参加者は自身のターミナル・RVizから任意の操作が可能です（ただしAWSIM画面は操作できません）。想定される操作は以下のとおりです。
    - Autowareの再起動
    - 自己位置の再設定
    - スタック時に、手動運転による車両の移動
    - `ros2 topic` コマンドによるギア切り替え・ターボコマンド発行
- ただし、操作前には運営に申告する必要があります。また、手動運転を多用することは禁止です。自身のROS_DOMAIN_ID以外に影響を及ぼす操作も禁止です。
