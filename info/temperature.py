import psutil


def temperature():
    try:
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                a = ("%.1f" % entry.current)
                temperature = (f"{a}°C")

                return temperature
    except Exception:
        temperature = (f"WRONG SYSTEM°C")
        return temperature
