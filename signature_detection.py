import psutil

# Define suspicious tools
blacklisted = [
    "AutoClicker.exe", "CheatEngine.exe", "TeamViewer.exe",
    "AnyDesk.exe", "obs64.exe", "vmtoolsd.exe", "VBoxService.exe"
]

def detect_cheating_tools():
    found = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] in blacklisted:
                found.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found

cheaters = detect_cheating_tools()
if cheaters:
    print("[ALERT] Possible cheating tools detected:")
    for proc in cheaters:
        print(proc)
else:
    print("System clean.")
