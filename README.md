
## 1. Connect to the Raspberry Pi (from your PC)

```bash
ssh pi@<raspberry-pi-ip>
# copy password when prompted
```

## 2. Copy the project to the Pi (from your PC)

```bash
scp -r . pi@<raspberry-pi-ip>:~/mikulska
```

## 3. Install dependencies on the Pi

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv docker.io docker-compose-plugin i2c-tools
```

## 4. Set up Python environment

```bash
cd ~/mikulska
python3 -m venv .venv
source .venv/bin/activate
pip install paho-mqtt smbus2 gpiozero
```

## 7. Run the project

```bash
cd ~/mikulska
source .venv/bin/activate
python main.py
```

Expected output: sensor readings every second (`eCO2`, `TVOC`, `temp`, `humidity`), data published to `team2/building/conference_room_1/air` every 15 readings.

## 8. Run in background (optional)

```bash
cd ~/mikulska
nohup .venv/bin/python main.py > main.log 2>&1 &
```