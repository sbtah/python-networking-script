#!/usr/bin/env python3
"""
Simple MAC changer script by Sbtah.
To run specify:
-i : interface that you want to change MAC address for,
-m : new MAC address for specified interface.

sudo python3 mc-ch.py -i <interface> -m <macaddress>
"""
import re
import subprocess
import optparse
import logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac_address", help="New MAC address.")
    options, arguments = parser.parse_args()

    return options.interface, options.new_mac_address

def get_current_mac(iface):
    raw_validate = subprocess.check_output(["ifconfig", interface])
    try:
        match = re.search(r"ether\s(\w{2}[:]\w{2}[:]\w{2}[:]\w{2}[:]\w{2}[:]\w{2})", str(raw_validate))
        current_mac = match.group(1)
    except AttributeError:
        logging.error("Can't find MAC address, is this a proper interface?.")
        return None
    else:
        return current_mac

def sexy_up_your_mc(iface, mcval):
    if iface is None or mcval is None: 
        logging.error("You have to provide interface (-i) and MAC (-m)")
    else:
        logging.info(f"Changing MAC address for: {iface} to address: {mcval}")
        logging.info("==" * 40)

        subprocess.run(["ifconfig", iface, "down"])
        subprocess.run(["ifconfig", iface, "hw", "ether", mcval])
        subprocess.run(["ifconfig", iface, "up"])

        current_mac = get_current_mac(iface)

    if current_mac and current_mac == mcval:
        return logging.info(f"Success, Your new MAC is: {current_mac}")
    else:
        return logging.error(f"Changing of MAC failed, your address: {current_mac}")


if __name__ == "__main__":
    interface, mac = get_args() 
    sexy_up_your_mc(interface, mac)