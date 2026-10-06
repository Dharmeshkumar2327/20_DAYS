"""
Python Program to Find IP Addresses
"""

import socket


def get_ip_address(hostname):
    """Return the IP address of a hostname."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


# Get local hostname
hostname = socket.gethostname()
print(f"Your Hostname is: {hostname}")

# Get local IP address
local_ip = get_ip_address(hostname)

if local_ip:
    print(f"Your IP Address is: {local_ip}")
else:
    print("Unable to find your IP address.")


# Get IP address of a website
host = "github.com"
host_ip = get_ip_address(host)

if host_ip:
    print(f"The IP Address of {host} is: {host_ip}")
else:
    print(f"Unable to find the IP address of {host}.")