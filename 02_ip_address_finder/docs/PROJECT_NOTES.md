# Project Notes

## Source Project

The uploaded program is titled **Python Program to Find IP Addresses** and uses Python's `socket` module.

The program:
1. Gets the local hostname with `socket.gethostname()`.
2. Resolves the hostname with `socket.gethostbyname()`.
3. Resolves `github.com` to an IPv4 address.
4. Handles DNS lookup failures using `socket.gaierror`.

## Educational Concepts

This is suitable as a beginner Python networking mini project covering functions, modules, exception handling, hostname resolution, DNS, and IPv4 addresses.

## Limitation

The program performs hostname resolution only. It does not scan ports or networks.
