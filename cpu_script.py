import psutil
import time

# Give it a moment to calculate CPU usage
for proc in psutil.process_iter():
    try:
        proc.cpu_percent(interval=None)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

# Wait a moment to get actual CPU usage values
time.sleep(1)

print("{:<8} {:<25} {:<10}".format("PID", "Name", "CPU %"))
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
    try:
        cpu = proc.info['cpu_percent']
        if cpu > 0:  # Only active processes
            print("{:<8} {:<25} {:<10}".format(
                proc.info['pid'],
                proc.info['name'] or "N/A",
                cpu
            ))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue
