sudo chmod +x server_yolo.py
sudo chmod +x server_yolo.log
nohup python3 server_yolo.py > server_yolo.log 2>&1 &
