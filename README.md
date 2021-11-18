# IoT (RPI)

Example code used at the 25th of November 2021 workshop.

# Usage

1. Install the git client and clone this repository

```bash
sudo apt install git
mkdir ~/git
cd ~/git
git clone https://github.com/mariolpantunes/rpi_iot.git
```

2. Install Mosquitto (MQTT broker)

```bash
sudo apt install mosquitto mosquitto-clients
```

3. Stop the broker and edit the configuration file

```bash
sudo systemctl stop mosquitto
sudo nano /etc/mosquitto/mosquitto.conf
```

4. Add the following lines:

```
allow_anonymous true
listener 1883 0.0.0.0

listener 9001 0.0.0.0
protocol websockets
```

5. Restart the broker

```bash
sudo systemctl start mosquitto
```

6. Install nginx to display the webpage

```
sudo apt install nginx-light
cd /var/www/html/
sudo ln -s /home/pi/git/rpi_iot/web/index.html index.html
```

7. Create a virtual enviroment and run the code

```bash
cd ~/git/rpi_iot/
python3 -m venv venv
source venv/bin/activate
CFLAGS="-fcommon" pip install -r rpi/requirements.txt
python rpi/main.py
```

8. Explore the MQTT messages with the application [MQTT-Explorer](http://mqtt-explorer.com/)

## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details