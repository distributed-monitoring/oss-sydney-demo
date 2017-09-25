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


* 正常時間帯、異常時間帯を指定した学習による異常通知デモ
# 今は単純な閾値判定にしかなっていない、
# analysis配下を色々いじって効果アピールできるものにしていく

 1. 正常な時間帯（何もしていない状態）をメモしておく
 $ N_STIME=$(date +"%F %T") ; sleep 10 ; N_ETIME=$(date +"%F %T")

 2. 異常な時間帯（stressでのメモリ負荷状態）をメモしておく
 $ python tools/stress_tools/mem_stress.py 3g 1 0 20 & \
   sleep 5 ; F_STIME=$(date +"%F %T") ; sleep 10 ; F_ETIME=$(date +"%F %T")

 3. 上記を指定して、learnコマンドを発行する
 $ python analysis/learn.py "${N_STIME}" "${N_ETIME}" "${F_STIME}" "${F_ETIME}"

 4. collectdを再起動する
 $ sudo systemctl restart collectd

 5. メモリ負荷をかけ、OpenStackへ通知が飛ぶことを確認する。
 $ python tools/stress_tools/mem_stress.py 3g 1 0 10


* （参考）今回におけるCongressの使い方

 * データの確認
 $ openstack congress datasource row list doctor events

 * データクリア
 $ openstack congress datasource row update doctor events '[]'


以上
