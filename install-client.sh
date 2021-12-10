#!/usr/bin/env bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Please run this script as root"
    exit
fi

if [[ -v DOWNLOADED ]]; then
  if [[ $DOWNLOADED == 0 ]]; then
    echo "Download complete"
    while fuser /var/lib/dpkg/lock >& /dev/null; do
      echo "waiting for other package installs to complete..."
      sleep 5
    done
    apt update
    apt install -y dialog iperf3 chromium-chromedriver python3-pip
    pip3 install -r requirements.txt
    echo "Enter server address"
    SERVER_ADDRESS=$(dialog --clear --title "Enter server address" --inputbox "Enter the connection address (IP or FQDN for your bandwidth-server)" 15 40 2>&1 >/dev/tty)

    echo "Server address: $SERVER_ADDRESS"

    echo "SERVER_ADDRESS=$SERVER_ADDRESS" | tee .env

    service="
    [Unit]
    Description=\"Bandwidth Client\"

    [Service]
    ExecStart=/usr/bin/python3 /root/bandwidth-client/main.py
    WorkingDirectory=/root/bandwidth-client
    Restart=always
    RestartSec=10
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=BandwidthClient

    [Install]
    WantedBy=multi-user.target
    "

    echo "$service" | sudo tee /etc/systemd/system/bandwidth-client.service

    sudo systemctl daemon-reload
    sudo systemctl enable bandwidth-client
    sudo systemctl start bandwidth-client

    exit 0
  fi
fi

mkdir bandwidth-client

cd bandwidth-client || exit

wget https://dl.techied.me/latest-client.tar.gz

tar -xvzf latest-client.tar.gz

rm latest-client.tar.gz

chmod +x install-client.sh

export DOWNLOADED=0
./install-client.sh
