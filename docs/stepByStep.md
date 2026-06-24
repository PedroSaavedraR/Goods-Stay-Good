install pi OS light (due to disk size constraint)
setup wifi (same network as computer)
setup ssh access (ssh into pi from computer)

usage: ssh pi@raspberrypi.local

on Pi:
➜  ~ ssh-keygen -t ed25519 -C "jelitaw-pi"
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/pi/.ssh/id_ed25519): 
Enter passphrase for "/home/pi/.ssh/id_ed25519" (empty for no passphrase): 
Enter same passphrase again: 
//no password
-> public key was added to Jelitaw GitHub Account

git clone git@github.com:PedroSaavedraR/Goods-Stay-Good.git
cd Goods-Stay-Good 

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```
Z-Wave USB Stick
        ↓
zwave-js-ui (Docker container)
        ↓ WebSocket (3000)
Python monitoring script
```


# Z-Wave Stack
➜  zwave-stack ls /dev/serial/by-id/
usb-0658_0200-if00
-> put this in the docker compose file

# For the backend server:
Install docker:
```
sudo apt remove -y docker-buildx

sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

cd zwave-stack
docker compose up -d

then in the venv start python script

then:
ssh -L 8091:localhost:8091 pi@raspberrypi.local

so that on the PC the website can be accessed:
http://localhost:8091/#/control-panel

Settings → Z-Wave -> Serial Port -> /dev/ttyACM0 -> Save, restart

-> Works in the Web UI, can connnect and read data (live) there

Now to get the data to python: use MQTT
install broker on pi:
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

check settings for MQTT in WebUI
Check&Debug with:  mosquitto_sub -t "zwave/#" -v


---

! TODO: update requirements file with:
pip freeze > requirements.txt
