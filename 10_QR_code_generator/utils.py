"""Payload validation, QR URI helpers, and small desktop utilities."""
import re
import webbrowser
import os
import subprocess
import sys

def build_payload(kind, raw):
    raw = raw.strip()
    if not raw:
        raise ValueError("Please enter content first.")
    if kind == "Website URL":
        if not re.match(r"^https?://", raw, re.IGNORECASE):
            raise ValueError("Website URLs must start with http:// or https://")
        return raw
    if kind == "Text":
        return raw
    if kind == "Email":
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", raw):
            raise ValueError("Enter a valid email address.")
        return f"mailto:{raw}"
    if kind == "Phone":
        phone = re.sub(r"[\s()-]", "", raw)
        if not re.match(r"^\+?\d{7,15}$", phone):
            raise ValueError("Enter a phone number with 7–15 digits.")
        return f"tel:{phone}"
    if kind == "SMS":
        phone = re.sub(r"[\s()-]", "", raw)
        if not re.match(r"^\+?\d{7,15}$", phone):
            raise ValueError("Enter a valid phone number with 7–15 digits.")
        return f"SMSTO:{phone}:"
    if kind == "Wi-Fi":
        parts = raw.split(";")
        if len(parts) != 3:
            raise ValueError("Wi-Fi format must be SSID;PASSWORD;WPA (or WEP/nopass).")
        ssid, password, security = parts
        security = security.upper()
        if security not in {"WPA", "WEP", "NOPASS"}:
            raise ValueError("Security must be WPA, WEP, or nopass.")
        if security == "NOPASS":
            return f"WIFI:T:nopass;S:{ssid};P:;;"
        return f"WIFI:T:{security};S:{ssid};P:{password};;"
    raise ValueError(f"Unsupported content type: {kind}")

def open_file(path):
    path = os.path.abspath(path)
    if sys.platform.startswith("win"):
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["open", path], check=False)
    else:
        subprocess.run(["xdg-open", path], check=False)

def copy_to_clipboard(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
