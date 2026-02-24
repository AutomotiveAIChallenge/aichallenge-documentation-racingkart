# 推奨環境

本大会で使用していただくPCの動作環境として以下を推奨しております。
推奨と書かれているものに関しては満たしていなくても動作することは可能です。ただし、推奨よりも低いスペックで動作させる場合ROS 2側での実行速度が安定せずシミュレーションの実行の度に挙動が大きく変わってしまう可能性があります。

!!! warning

    Windows環境しかお持ちでない方は、Ubuntu22.04のインストールをお願いいたします。Windows環境と同じディスクにUbuntu環境を入れることもできますが、不慣れな場合Windows環境を破壊してしまう可能性があるため、新しく外付けまたは内蔵SSDを購入したうえでそちらへのインストールをすることを強くお勧めします。

!!! info

    Ubuntuのインストール方法については[こちらの記事](https://qiita.com/kiwsdiv/items/1fa6cf451225492b33d8)が参考になります。

## 描画なしのAWSIMを使用する場合

- OS: Ubuntu 22.04
- CPU: Intel Core i5（4コア）以上（推奨）
- メモリ:
  - 8GB以上（最低）
  - 16GB以上（推奨）
- SSD: 60GB以上

## 描画ありのAWSIMを使用する場合

- OS: Ubuntu 22.04
- CPU: Intel Corei7 (8 cores) or higher
- GPU: NVIDIA Geforce VRAM 8 GB
- Memory: 16 GB or more
- Storage: SSD 60 GB or higher

## [Next Step: 環境構築の流れ](./introduction.ja.md)
