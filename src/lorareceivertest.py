import os
import glob
import shutil
import serial
import time
from datetime import datetime

# ───── CONFIG ─────
LABELS = [
    "Elapsed [s]",
    "Temp_BME280 [°C]", "Hum [%]", "Press [hPa]", "Alt [m]",
    "Acc x [m/s²]", "Acc y [m/s²]", "Acc z [m/s²]",
    "Gyro x [°/s]", "Gyro y [°/s]", "Gyro z [°/s]",
    "Temp_MPU [°C]"
]
DECIMALS = [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
MIN_COLUMNS = len(LABELS) + 1

COM_PORT = 'COM8'     # Adjust if needed
BAUD_RATE = 9600
LOG_DIR = "logs"
ARCHIVE_DIR = os.path.join(LOG_DIR, "previous_data")

# ───── PREPARE LOGGING ─────
os.makedirs(ARCHIVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

for file in glob.glob(os.path.join(LOG_DIR, "sensor_data_*.csv")):
    shutil.move(file, ARCHIVE_DIR)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logfile = os.path.join(LOG_DIR, f"sensor_data_{timestamp}.csv")

with open(logfile, "w") as f:
    header = f"{'Timestamp (MET)':<22}" + "".join(
        f"{label:>{DECIMALS[i] + 14}}" for i, label in enumerate(LABELS)
    ) + "\n"
    f.write(header)

print(f"📂 Logging to: {logfile}")

# ───── INIT SERIAL ─────
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"🔌 Connected to {COM_PORT} at {BAUD_RATE} baud.")
except Exception as e:
    print("❌ Serial error:", e)
    exit(1)

# ───── INIT DATA CONTAINERS ─────
min_data = [float('inf')] * len(LABELS)
max_data = [float('-inf')] * len(LABELS)

print("📡 Listening for LoRa data...")

try:
    while True:
        if ser.in_waiting:
            line = ser.readline().decode(errors='ignore').strip()

            if not line or line.count(",") < MIN_COLUMNS - 1:
                print("⚠️ Skipped incomplete line:", line)
                continue

            print("📥", line)

            fields = line.split(",")
            try:
                float_data = [float(f) for f in fields[1:]]  # Skip timestamp
                for i, val in enumerate(float_data):
                    min_data[i] = min(min_data[i], val)
                    max_data[i] = max(max_data[i], val)
            except:
                pass  # If parsing fails, skip min/max update

            # Align and log line
            with open(logfile, "a") as f:
                f.write(f"{fields[0]:<22}")
                for i in range(len(LABELS)):
                    try:
                        val = float(fields[i + 1])
                        f.write(f"{val:>{DECIMALS[i] + 14}.{DECIMALS[i]}f}")
                    except:
                        f.write(f"{fields[i + 1]:>{DECIMALS[i] + 14}}")
                f.write("\n")

except KeyboardInterrupt:
    print("\n🛑 Gracefully stopped. Writing min/max summary...")

    with open(logfile, "a") as f:
        min_line = "MIN" + " " * 18
        max_line = "MAX" + " " * 18

        for i in range(len(LABELS)):
            try:
                min_line += f"{min_data[i]:>{DECIMALS[i] + 14}.{DECIMALS[i]}f}"
                max_line += f"{max_data[i]:>{DECIMALS[i] + 14}.{DECIMALS[i]}f}"
            except:
                min_line += f"{'':>{DECIMALS[i] + 14}}"
                max_line += f"{'':>{DECIMALS[i] + 14}}"

        f.write("\n" + min_line + "\n" + max_line + "\n")
    print("✅ Min/max summary written to log.")
