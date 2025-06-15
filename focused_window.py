import time
import win32gui

# Define your app and Chrome as allowed apps
allowed_windows = ["Google Chrome", "MyAppName"]  # Change "MyAppName" to your actual app's window title

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

last_title = get_active_window_title()

while True:
    current_title = get_active_window_title()
    if current_title != last_title:
        print(f"[INFO] Window changed: {current_title}")
        if not any(allowed in current_title for allowed in allowed_windows):
            print("[ALERT] Focus moved away from allowed apps!")
        last_title = current_title
    time.sleep(1)
