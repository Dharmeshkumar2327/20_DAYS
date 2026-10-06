# IP Address Finder using Python

A beginner-friendly Python mini project that uses the built-in `socket` module to find the IP address associated with a hostname.

The project demonstrates two practical tasks:

- Find the local computer hostname and its IP address.
- Find the IP address of a website such as `github.com`.

## Project Overview

The original mini project uses Python's `socket.gethostbyname()` function and handles DNS lookup errors with `socket.gaierror`.

## Features

- Get the local hostname
- Resolve the local hostname to an IP address
- Resolve a website hostname to an IPv4 address
- Basic exception handling
- Uses only Python's standard library

## Technologies Used

- Python 3
- `socket` module
- DNS hostname resolution

## Requirements

Python 3.8+ is recommended.

No third-party packages are required.

## Project Structure

```text
ip-address-finder/
│
├── src/
│   └── ip_address_finder.py
│
├── examples/
│   └── 02_IP_Address_find_mini_projecct.py
│
├── docs/
│   └── PROJECT_NOTES.md
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## How to Run

From the project root:

```bash
python src/ip_address_finder.py
```

On some systems, use:

```bash
python3 src/ip_address_finder.py
```

## Example Output

```text
Your Hostname is: YOUR-COMPUTER-NAME
Your IP Address is: 192.168.x.x
The IP Address of github.com is: <resolved-ip>
```

The actual IP address can change depending on your network, DNS resolver, and the website's infrastructure.

## How the Program Works

### 1. Import socket

```python
import socket
```

The `socket` module provides networking functions, including hostname-to-IP resolution.

### 2. Create an IP lookup function

```python
def get_ip_address(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None
```

`socket.gethostbyname()` resolves a hostname to an IPv4 address.

### 3. Get the local hostname

```python
hostname = socket.gethostname()
```

This returns the computer's network hostname.

### 4. Resolve the hostname

```python
local_ip = get_ip_address(hostname)
```

The program attempts to convert the hostname into an IPv4 address.

### 5. Resolve a website

```python
host = "github.com"
host_ip = get_ip_address(host)
```

The same function can resolve a public hostname.

## Learning Objectives

After completing this project, you should understand:

- Python modules
- The `socket` module
- Hostnames and IP addresses
- DNS hostname resolution
- Functions
- `try` / `except`
- `socket.gaierror`
- Conditional statements
- Basic computer networking concepts

## Important Note

This project performs hostname resolution. It does **not** perform network scanning, port scanning, or security testing.

## Suggested GitHub Topics

```text
python
socket
ip-address
networking
dns
python-project
beginner-python
computer-networking
```

## Short GitHub Description

A beginner-friendly Python networking mini project that uses the socket module to find the local hostname, local IP address, and IPv4 address of a website such as GitHub.

## Author

Dharmesh Kumar

## License

This project is provided for educational and learning purposes.
