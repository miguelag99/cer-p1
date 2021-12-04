sudo systemctl start elasticsearch.service
python3 server_logic.py &
sudo python3 presentation_layer.py
