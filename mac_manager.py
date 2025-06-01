#!/usr/bin/env python3
import os
import platform
import time
import re
import json
import subprocess

HISTORY_FILE = "mac_history.json"
def setup():
    print("Setting up...")
    print("Python Version:", platform.python_version())
    print("Operating System:", platform.system())
    if platform.system() == "Linux":
        return True
        # print("Starting mac_changer_linux.py...")
        # os.system("python3 mac_changer_linux.py")
    else:
        print("System not supported!")
        return False

def get_network_interface():
    """ Returns a list of network interfaces """ 
    result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
    interfaces = re.findall(r"\d+: (\w+):", result.stdout)
    return interfaces   

def load_mac_history():
    """ Returns a dictionary of previously saved mac addresses """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return {}

def save_mac_to_history_old(interface, mac_address, description=""):
    """ Saves a mac address to the history file """
    history = load_mac_history()
    if interface not in history:
        history[interface] = {"description": description, "mac_address": []}
    
    if description:
        history[interface]["description"] = description

    if mac_address not in history[interface]["mac_address"]:
        history[interface]["mac_address"] = mac_address
        history[interface]["description"] = description
        print(f"[INFO] Mac address {mac_address} saved to history\n for interface {interface} with description {description}")

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def change_mac(interface, new_mac):
    """ Changes the MAC address of a network interface """
    print(f"[INFO] Changing MAC address {new_mac} for interface {interface}...")
    os.system(f"sudo ip link set dev {interface} down")
    os.system(f"sudo ip link set dev {interface} address {new_mac}")
    os.system(f"sudo ip link set dev {interface} up")
    # save_mac_to_history(interface, new_mac)
    print("[INFO] Restarting NetworkManager...")
    print("If Errors arises pleas manually restart Network Manager service or restart computer")
    os.system(f"sudo systemctl restart NetworkManager.service")
    print("[OK] NetworkManager restarted successfully!")
    print("[OK] Address changed successfully!")

def change_mac_windows(interface, new_mac):
    """ Zmienia adres MAC na Windows za pomocą netsh 
    This has not been tested for windows, 
    if sm wants to  test then do it in python not in binary
    """
    print(f"[INFO] Zmieniam MAC na {new_mac} dla interfejsu {interface}...")
    
    os.system(f"reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\{interface} /v NetworkAddress /t REG_SZ /d {new_mac} /f")
    os.system("ipconfig /release")
    os.system("ipconfig /renew")
    
    print("[OK] Adres MAC zmieniony! Restart komputera może być wymagany.")


def show_mac_history(interface):
    """ Shows a list of previously saved mac addresses """
    history = load_mac_history()
    if interface in history:
        print("\nHistory for interface", interface)
        for i, mac in enumerate(history[interface]["mac_addresses"]):
            print(f"{i + 1}. {mac}")
        return history[interface]
    else:
        print("\nNo history found.")
        return []

def save_mac_to_history(interface, mac_address, description):
    data = load_mac_history()

    if interface not in data:
        data[interface] = {"mac_addresses": []}

    for entry in data[interface]["mac_addresses"]:
        if entry["address"] == mac_address:
            entry["description"] = description
            break
    else:
        data[interface]["mac_addresses"].append({
            "address": mac_address,
            "description": description
        })
    with open(HISTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)
        

def update_addres_mac_history(interface, old_address, new_address):
    data = load_mac_history()
    for entry in data[interface]["mac_addresses"]:
        if entry["address"] == old_address:
            entry["address"] = new_address
            break

    with open(HISTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

def update_desc_mac_history(interface, mac_address, desc):
    data = load_mac_history()
    for entry in data[interface]["mac_addresses"]:
        if entry["address"] == mac_address:
            entry["description"] = desc
            break

    with open(HISTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def rm_entry_from_history(interface, mac_address):
    data = load_mac_history()

    for entry in data[interface]["mac_addresses"]:
        if entry["address"] == mac_address:
            data[interface]["mac_addresses"].remove(entry)
            break

    with open(HISTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

def check_mac(mac_address):
    """ Checks if a mac address is valid """
    x = re.match(r"^[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}$", mac_address.lower())
    if x is not None:
        return True
    else:
        return False

def get_mac_address(interface):
    """ Returns the current MAC address of a network interface """
    result = subprocess.run(["cat", f"/sys/class/net/{interface}/address"], capture_output=True, text=True)
    return result.stdout
def main():
    #main menu
    while True:
        print("Mac Changer Menu")
        print("================")
        print("Options:")
        print("1. input new mac addres")
        print('2. choose mac addres from history')
        print('3. update mac addres in history')
        print("4. show history")
        print("5. show my mac address")
        print("6. save current mac addresses to history")
        print("q. exit")
        choice = input("Choose number 1-6 or q to exit: ")
        # podzielić to na funkcje screenM() screen1() itp bo będą błędy związane z nazwami funkcji
        if choice == "1":
            while True:
                os.system("clear")
                print("Inputing new mac address...")
                # print(get_network_interface())
                subprocess.run(["ip", "link", "show"])
                while True:
                    interface = input("Enter interface name: ")
                    if interface in get_network_interface():
                        break
                    else:
                        print("Interface not found!")
                while True:
                    mac_address = input("Enter new mac address: ")
                    if check_mac(mac_address):
                        break
                    else:
                        print("Invalid mac address!")
                description = input("Enter description: ")
                print(f"New mac address will be:, {mac_address}" + "\n" + f"Interface:, {interface}" + "\n" + f"Description:, {description}")
                save = input("Do you want to save this mac address to history? (y/n): ")
                if save == "y":
                    change_mac(interface, mac_address)
                    save_mac_to_history(interface, mac_address, description)
                    break
                elif save == "n":
                    change_mac(interface, mac_address)
                    break
                else:
                    print("Invalid input!")
                    time.sleep(2)
        
        elif choice == "2":
            while True:
                os.system("clear")
                print("Choose mac address from history:")
                for interface in list(load_mac_history().keys()):
                        show_mac_history(interface)
                history = load_mac_history()
                flag = False
                while True:
                    interface = input("Enter interface name: ")
                    if interface in history:
                        break
                    elif interface == "q":
                        flag = True
                        break
                    else:
                        print("Interface not found!")
                if flag:    
                    break

                while True:
                    os.system("clear")
                    print("Choose mac address from history:")
                    for i, mac in enumerate(history[interface]["mac_addresses"]):
                        print(f"{i + 1}. {mac}")
                    mac_num = input("Enter mac address number: ")
                    if mac_num.isdigit() and int(mac_num) -1 <= len(history[interface]["mac_addresses"]):
                        break
                    elif mac_num == "q":
                        flag = True
                        break
                    else:
                        print("Invalid input!")
                if flag:
                    break

                print(f"Selected mac address: {history[interface]['mac_addresses'][int(mac_num) - 1]['address']}")
                update = input("Do you want to choose this mac address? (y/n): ")
                if update == "y":
                    change_mac(interface, history[interface]['mac_addresses'][int(mac_num) - 1]['address'])
                    break
                elif update == "n":
                    break
                elif update == "q":
                    break
                else:
                    print("Invalid input!")

        elif choice == "3":
            while True:
                os.system("clear")
                print("Choose mac address to update:")
                for interface in list(load_mac_history().keys()):
                        show_mac_history(interface)
                history = load_mac_history()
                flag = False
                while True:
                    print("q. back")
                    interface = input("Enter interface name: ")
                    if interface in history:
                        break
                    elif interface == "q":
                        flag = True
                        break
                    else:
                        print("Interface not found!")
                if flag:
                    break

                while True:
                    os.system("clear")
                    print("Choose mac address to update:")
                    for i, mac in enumerate(history[interface]["mac_addresses"]):
                        print(f"{i + 1}. {mac}")
                    print("q. back")
                    mac_choice = input("Enter mac address number: ")
                    if mac_choice.isdigit() and int(mac_choice) -1 <= len(history[interface]["mac_addresses"]):
                        break
                    elif mac_choice == "q":
                        flag = True
                        break
                    else:
                        print("Invalid input!")
                if flag:
                    break
                os.system("clear")
                print(f"Selected mac address: {history[interface]['mac_addresses'][int(mac_choice) - 1]['address']}")
                while True:
                    print("1. Update mac address")
                    print("2. Update description")
                    print("3. Update both")
                    print("4. Remove entry")
                    print("q. back")
                    choice3 = input("Enter choice: ")
                    if choice3 == "1":
                        while True:
                            mac_address = input("Enter new mac address: ")
                            if check_mac(mac_address):
                                break
                            else:
                                print("Invalid mac address!")
                        update_addres_mac_history(interface, history[interface]['mac_addresses'][int(mac_choice) - 1]['address'], mac_address)
                        break
                    elif choice3 == "2":
                        description = input("Enter new description: ")
                        update_desc_mac_history(interface, history[interface]['mac_addresses'][int(mac_choice) - 1]['address'], description)
                        break
                    elif choice3 == "3":
                        while True:
                            mac_address = input("Enter new mac address: ")
                            if check_mac(mac_address):
                                break
                            else:
                                print("Invalid mac address!")
                        description = input("Enter new description: ")
                        update_desc_mac_history(interface, history[interface]['mac_addresses'][int(mac_choice) - 1]['address'], description)
                        update_addres_mac_history(interface, history[interface]['mac_addresses'][int(mac_choice) - 1]['address'], mac_address)
                        break
                    elif choice3 == "4":
                        rm_entry_from_history(interface, history[interface]['mac_addresses'][int(mac_choice) - 1]['address'])
                        break
                    elif choice3 == "q":
                        break
                    else:
                        print("Invalid input!")          

        elif choice == "4":        
            while True:
                os.system("clear")
                print("All Interfaces:")
                print((str(list(load_mac_history().keys()))), str(get_network_interface()))
                print("Select interface:")
                print("a. all")
                print("q. back")
                choice4 = input("Enter name of interface or command: ")
                if choice4 == "a":
                    for interface in list(load_mac_history().keys()):
                        show_mac_history(interface)
                    input("press anything to go back: ")
                elif choice4 == "q":
                    break
                elif choice4 in get_network_interface():
                    show_mac_history(choice4)
                    input("press anything to go back: ")
                    break
                else:
                    print("Invalid input!")
                    time.sleep(2)
        elif choice == "5":
            while True:
                os.system("clear")
                subprocess.run(["ip", "link", "show"])
                choice5 = input ("press q to go back: ")
                if choice5 == "q":
                    break
                else:
                    print("Invalid input!")
        elif choice == "6":
            os.system("clear")
            print("Saving mac addresses to history...")
            desc = input("Enter description: ")
            for interface in get_network_interface():
                save_mac_to_history(interface, get_mac_address(interface).rstrip("\n"), desc)
            print("Mac addresses saved to history!")
            input("press anything to go back: ")
            os.system("clear")


        elif choice == "q":
            exit(0)
        else:
            print("Invalid input!")

    
if __name__ == "__main__":
    setup_v = setup()
    if setup_v == False:
        print("Setup failed!")
        exit(1)
    else:
        print("Setup successful!")
        time.sleep(1)
        os.system("clear")
        interfaces = get_network_interface()
        if not interfaces:
            print("No network interfaces found.")
            exit(1)
        main()        
