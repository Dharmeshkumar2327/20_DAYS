"""Find the IPv4 address of a website hostname."""

import socket


def get_hostname_ip():
    hostname = input("Please enter website address (e.g., google.com): ").strip()

    if not hostname:
        print("Please enter a valid hostname.")
        return

    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
    except socket.gaierror as error:
        print(f"Invalid Hostname. Error: {error}")


if __name__ == "__main__":
    get_hostname_ip()
