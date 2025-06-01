# MAC Address Changer

A Python-based tool to manage and modify MAC addresses for network interfaces on Linux systems. This program allows users to change MAC addresses, save them to history, update descriptions, and manage previously saved MAC addresses.

## Features

- Change the MAC address of a network interface.
- Save MAC addresses with descriptions to a history file (`mac_history.json`).
- Update MAC addresses or descriptions in the history.
- Remove MAC addresses from the history.
- View the current MAC address of network interfaces.
- Display and manage the history of saved MAC addresses.

## Requirements

- Python 3.x
- Linux operating system
- `ip` command (part of `iproute2` package)
- `sudo` privileges to modify MAC addresses
- `NetworkManager` service (optional, for restarting the network)

## One time run

1. Download mac_manager.py and run it:
   ```bash
   chmod +x mac_manager.py
   python mac_manager.py

## Permament setup for quick use

1. Add permissions
```bash
  chmod +x mac_manager.py
```
2. Create global command:
```bash
sudo mv mac_manager.py /usr/local/bin/mac_manager
```
3. Run program:
```bash
mac_manager
```


  
