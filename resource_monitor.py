import psutil
import time

cpu_history = []
mem_history = []
timestamps = []


N = 60  
total_duration = 100 

start_time = time.time()

print("Monitoring system resource usage (CPU and Memory)...\n")

for _ in range(total_duration):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    mem_used_percent = (mem.used / mem.total) * 100

    current_time = int(time.time() - start_time)
    timestamps.append(current_time)
    cpu_history.append(cpu)
    mem_history.append(mem_used_percent)

    timestamps = timestamps[-N:]
    cpu_history = cpu_history[-N:]
    mem_history = mem_history[-N:]

    print(f"Time: {current_time}s | CPU Usage: {cpu:.2f}% | Memory Usage: {mem_used_percent:.2f}%")

print("\nMonitoring complete.")
