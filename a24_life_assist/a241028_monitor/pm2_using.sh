
TZ='Asia/Shanghai'
tzselect
ntpdate cn.pool.ntp.org
# hwclock --systohc

pm2 stop server_yolo
pm2 delete server_yolo
# pm2 start -n server_yolo '/home/nano/server_yolo.py'
# echo '/usr/bin/python /data/pn-2/codes/a24_life_assist/a241028_monitor/server_yolo.py' > ~/.cache/server_yolo.sh
pm2 start -n server_yolo '/data/pn-2/codes/a24_life_assist/a241028_monitor/server_yolo.py'
pm2 save
# pm2 startup server_yolo
# sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup server_yolo -u nano --hp /home/nano
# # or:
pm2 startup
sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u nano --hp /home/nano


# pm2 restart server_yolo


