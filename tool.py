# tool.py — Secure WAN Chat Client by Abdul Ghaniy

import socket
import threading
import sys
import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# === Color Codes ===
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"

# === Encryption Setup ===
KEY = hashlib.sha256(b"ghaniykey").digest()
IV = b"1234567890123456"

# === Encoding Maps ===
ENCODE_MAP = str.maketrans("0123456789.", "gjapqtrbvwX")
DECODE_MAP = str.maketrans("gjapqtrbvwX", "0123456789.")

def encrypt(msg):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return base64.b64encode(cipher.encrypt(pad(msg.encode(), AES.block_size))).decode()

def decrypt(msg):
    try:
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        return unpad(cipher.decrypt(base64.b64decode(msg)), AES.block_size).decode()
    except:
        return ""

def decode_ip(encoded):
    return encoded.translate(DECODE_MAP)

def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass  # Fix Termux permission issue

def print_banner():
    print(rf"""{CYAN}
   _____ _           _       _____ _           _
  / ____| |         | |     / ____| |         | |
 | |    | |__   __ _| |_   | |    | |__   __ _| |_
 | |    | '_ \ / _` | __|  | |    | '_ \ / _` | __|
 | |____| | | | (_| | |_   | |____| | | | (_| | |_
  \_____|_| |_|\__,_|\__|   \_____|_| |_|\__,_|\__|
{RESET}""")
    print(f"{CYAN}{BOLD}Welcome to the Secure WAN Chat Tool! by Abdul Ghaniy{RESET}\n")

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(2048).decode()
            print(f"{CYAN}{decrypt(msg)}{RESET}")
        except:
            print(f"{RED}[ERROR] Lost connection to server.{RESET}")
            sock.close()
            sys.exit()

def start_client(ip, port, username):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        print(f"{GREEN}[CONNECTED] Connected successfully!{RESET}\n")
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

        sock.send(encrypt(username).encode())

        while True:
            msg = input(f"{YELLOW}{username}: {RESET}")
            if msg.lower() == 'exit':
                print(f"{RED}[EXITING] Goodbye.{RESET}")
                sock.close()
                break
            elif msg.lower().startswith('@file'):
                print(f"{GREEN}[FEATURE] File sharing coming soon!{RESET}")
                continue
            sock.send(encrypt(msg).encode())
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

# === Entry Point ===
if __name__ == "__main__":
    clear_screen()
    print_banner()

    username = input(f"{GREEN}Enter your username: {RESET}")
    conn_code = input(f"{CYAN}Enter connection code (e.g. xxxxxxxx:xxxx): {RESET}")


    try:
        encoded_ip, encoded_port = conn_code.strip().split(":")
        decoded_ip = decode_ip(encoded_ip)
        decoded_port = int(decode_ip(encoded_port))
    except:
        print(f"{RED}[ERROR] Invalid connection code format. Use: code:port{RESET}")
        sys.exit()

    start_client(decoded_ip, decoded_port, username)

