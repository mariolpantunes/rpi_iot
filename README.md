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
```

```bash
CFLAGS="-fcommon" pip install -r requirements.txt
```


## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details