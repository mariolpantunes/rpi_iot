# IoT (RPI)

Example code used at the 11th of November 2021 workshop.

# Usage

1. Install Mosquitto (MQTT broker)

```bash
sudo apt install mosquitto mosquitto-clients
```

2. Stop the broker and edit the configuration file

```bash
sudo systemctl stop mosquitto
sudo nano /etc/mosquitto/mosquitto.conf
```

3. Add the following lines:

```
allow_anonymous true
listener 1883 0.0.0.0

listener 9001 0.0.0.0
protocol websockets
```

4. Restart the broker

```bash
sudo systemctl start mosquitto
```

5. Install nginx to display the webpage

```
sudo apt install nginx-light
cd /var/www/html/
sudo ln -s /home/pi/git/rpi_iot/web/index.html index.html
```

6. Create a virtual enviroment and run the code

```bash
python3 -m venv venv
source venv/bin/activate
CFLAGS="-fcommon" pip install -r rpi/requirements.txt
python rpi/main.py
```

7. Explore the MQTT messages with the application [MQTT-Explorer](http://mqtt-explorer.com/)

## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details