
## 1. Connect to the Raspberry Pi (from your PC)

```bash
ssh pi@<raspberry-pi-ip>
# copy password when prompted
```

## 2. Copy the project to the Pi (from your PC)

```bash
scp -r . pi@<raspberry-pi-ip>:~/mikulska
```

```bash
cd ~/Desktop/mikulska
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install paho-mqtt smbus2 gpiozero pillow
python main.py
```