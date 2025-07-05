# secure_server.py — Stealth WAN Chat Server by Abdul Ghaniy

import socket
import threading
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

clients = []
client_names = {}
group_chats = {}

KEY = hashlib.sha256(b"ghaniykey").digest()
IV = b"1234567890123456"

# Encode map
def encode_ip(ip):
    return ip.translate(str.maketrans("0123456789.", "gjapqtrbvwX"))

def decode_ip(encoded_ip):
    return encoded_ip.translate(str.maketrans("gjapqtrbvwX", "0123456789."))

# AES Encrypt/Decrypt
def encrypt(msg):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return base64.b64encode(cipher.encrypt(pad(msg.encode(), AES.block_size))).decode()

def decrypt(msg):
    try:
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        return unpad(cipher.decrypt(base64.b64decode(msg)), AES.block_size).decode()
    except:
        return ""

# Broadcast to others
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

# Handle each client
def handle_client(sock):
    try:
        sock.send(encrypt("Enter your name: ").encode())
        name = decrypt(sock.recv(1024).decode())
        client_names[sock] = name
        broadcast(encrypt(f"[INFO] {name} joined the chat."), sock)

        while True:
            encrypted_msg = sock.recv(2048).decode()
            msg = decrypt(encrypted_msg)

            if msg.startswith("@group"):
                group = msg.split()[1]
                group_chats.setdefault(group, []).append(sock)
                sock.send(encrypt(f"[GROUP] Joined group: {group}").encode())

            elif msg.startswith("@file:"):
                broadcast(encrypt(f"{name}: {msg}"), sock)

            else:
                broadcast(encrypt(f"{name}: {msg}"), sock)
    except:
        pass
    finally:
        if sock in clients:
            clients.remove(sock)
        if sock in client_names:
            del client_names[sock]
        sock.close()

# Start server
if __name__ == "__main__":
    try:
        port = int(input("Set a secure port (e.g. 9090): "))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevent port-in-use crash
        server.bind(('0.0.0.0', port))
        server.listen()

        ip = socket.gethostbyname(socket.gethostname())
        encoded_ip = encode_ip(ip)
        encoded_port = encode_ip(str(port))

        print("\n🔐 Server launched securely.")
        print(f"🔗 Connection Code (for client use only):\n\n   {encoded_ip}:{encoded_port}\n")

        while True:
            sock, _ = server.accept()
            clients.append(sock)
            threading.Thread(target=handle_client, args=(sock,), daemon=True).start()
    except OSError as e:
        if e.errno == 98:
            print("❌ Port already in use. Try a different one.")
        else:
            print(f"[ERROR] {e}")
    except Exception as e:
        print(f"[CRASH] {e}")

