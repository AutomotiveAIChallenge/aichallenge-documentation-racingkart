# ハードウェア

## センサ構成

| センサ | モデル / 仕様 | 役割 |
| --- | --- | --- |
| GNSS | u-blox ZED-F9R | 衛星測位による車両の緯度・経度・高度の取得 |
| IMU | ICM-20948 | 加速度・角速度の計測（車両の姿勢や回転の検出） |

予選では AWSIM 上の仮想センサとして再現されます。

## PC構成 (車両搭載PC)

| 項目 | スペック |
| --- | --- |
| CPU | Intel Core i9-11900H |
| Mem | 32 GB |
| 備考 | 車両制御ソフトウェアも同じECU上で動きます |

## PC構成 (SIM予選環境)

| 項目 | スペック |
| --- | --- |
| CPU | 16 vCPU Intel Xeon Scalable (Cascade Lake) |
| Mem | 64 GB |
| 備考 | Autoware用には3 vCPUと12 GiBが割り当てられます |
