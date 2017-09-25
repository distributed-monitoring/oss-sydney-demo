* デモインストール手順
 1. OpenStack認証情報を設定する。
   $ vi dma.conf
  (以下、write_congressの中身を設定する)

<Plugin python>
        (...中略...)
        <Module "write_congress">
            Username "admin"
            Password "pass"
            TenantName "admin"
            AuthURL "http://192.168.1.3:5000/v2.0"
        </Module>
</Plugin>

 2. インストール実行
   $ ./installer.sh

 3. stressコマンドインストール（アプリとしてstressを使う場合）
   $ sudo yum install stress


* stressコマンドによるメモリリーク検出デモ

 1. メモリを一括確保し、Congressへ通知がいかないことを見せる
 $ python tools/stress_tools/mem_stress.py 200m 16 0 5

 2. メモリを徐々に確保し、Congressへ通知がいくことを見せる
 $ python tools/stress_tools/mem_stress.py 200m 16 0.7 5


* （参考）今回におけるCongressの使い方

 * データの確認
 $ openstack congress datasource row list doctor events

 * データクリア
 $ openstack congress datasource row update doctor events '[]'


以上
