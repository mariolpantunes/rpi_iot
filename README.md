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

5. Create a virtual enviroment and run the code

```bash
python3 -m venv venv
source venv/bin/activate
CFLAGS="-fcommon" pip install -r requirements.txt
python main.py
```


## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details