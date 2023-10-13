# donkeytank
donkey tank

## setup

donkeycar 5.0.dev3 (git checkout main)

setup on bullseye (Legacy 2023-05-03) because of python3.9

```bash
sudo apt update && sudo apt upgrade -y && sudo raspi-config
```

I2C, Legacy Camera, Pigpio, Expand Filesystem and reboot.

```bash
sudo apt-get install build-essential python3 python3-dev python3-pip python3-virtualenv python3-numpy python3-picamera python3-pandas python3-rpi.gpio i2c-tools avahi-utils joystick libopenjp2-7-dev libtiff5-dev gfortran libatlas-base-dev libopenblas-dev libhdf5-serial-dev libgeos-dev git ntp

pip install virtualenv
python3 -m virtualenv -p python3 env --system-site-packages
echo "source ~/env/bin/activate" >> ~/.bashrc
source ~/.bashrc
cd
mkdir projects
cd projects

git clone https://github.com/autorope/donkeycar
mv donkeycar donkeycar5
cd donkeycar5
git checkout main
pip install -U pip setuptools wheel
# install with tensorflow 2.9.0 with Python3.9
pip install -e .[pi]
```
