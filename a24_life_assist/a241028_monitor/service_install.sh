
systemctl stop "$name.service"
systemctl disable "$name.service"

name="server_yolo"
cmd=/usr/bin/python3 /home/nano/server_yolo.py

# sudo vi "/etc/systemd/system/$name.service"


echo "[Unit]
Description=$name
After=network.target

[Service]
User=nano
WorkingDirectory=/home/nano/
ExecStart=$cmd
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=$name

[Install]
WantedBy=multi-user.target
" > "/etc/systemd/system/$name.service"



systemctl enable "$name.service"
systemctl start "$name.service"

systemctl status "$name.service"
