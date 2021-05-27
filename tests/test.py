import psutil


print(psutil.sensors_temperatures())
cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0]
print(cpu_temp.current)

