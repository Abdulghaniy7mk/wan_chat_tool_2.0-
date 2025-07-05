
---

# 💬 Secure WAN Chat Tool 2.0

**Secure WAN Chat Tool** is a fast and private command-line chat application built by **Abdul Ghaniy**. It allows encrypted communication between multiple users over LAN or WAN using a simple connection code, not real IPs or ports.

It supports **AES encryption**, **group chat**, and works smoothly on **Termux**, **Windows**, and **Linux**.

---

## ⚙️ Features

* ✅ End-to-end AES encryption (with `privacykey` key)
* ✅ Connect using a **private connection code**
* ✅ Real-time multi-user chat
* ✅ Colorful terminal UI (CLI)
* ✅ Cross-platform: Termux / Linux / Windows

---

## 📦 Requirements

* Python 3.8 or higher
* Install dependencies:

  ```bash
  pip install pycryptodome
  ```

---

## 📲 Installation

### 📱 Termux

```bash
pkg update && pkg upgrade
pkg install python git
pip install pycryptodome
git clone https://github.com/Abdulghaniy7mk/wan_chat_tool_2.0-.git
cd wan_chat_tool_2.0-
```

### 🖥️ Windows

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Open Command Prompt or PowerShell:

```bash
git clone https://github.com/Abdulghaniy7mk/wan_chat_tool_2.0-.git
cd wan_chat_tool_2.0-
pip install pycryptodome
```

### 🐧 Linux

```bash
sudo apt update && sudo apt install python3 git
pip install pycryptodome
git clone https://github.com/Abdulghaniy7mk/wan_chat_tool_2.0-.git
cd wan_chat_tool_2.0-
```

---

## 🚀 How to Use

### 1. Start the Server

Run the server script and choose a port:

```bash
python secure_server.py
```

Example output:

```
✅ Server started successfully
🔗 Share this connection code:
   xxxxxxxx:xxxx
```

### 2. Connect as a Client

Run the client tool:

```bash
python tool.py
```

Then:

* Enter your **username**
* Paste the **connection code** given by the server

---

## 🛠️ Troubleshooting

### "Connection refused"

* Make sure the server is running and port is not blocked.

### "Permission denied" on Termux

```bash
termux-setup-storage
chmod +x tool.py secure_server.py
```

### "Address already in use"

* Try another port like `8080`, `9191`, etc.

---

## 📝 License

This project is licensed under the **MIT License**.
Made with 💙 by **Abdul Ghaniy**

---
