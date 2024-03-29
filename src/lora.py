import sys
import sx126x
import termios
import tty
import time
import select
import threading
from threading import Timer
import numpy as np

# Existing setup code
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())
# Assuming the frequency should be in Hz and the library expects an integer

node = sx126x.sx126x(serial_num="/dev/ttyS0", freq=868, addr=0, power=22, rssi=True, air_speed=2400, relay=False)

data = np.zeros(12)


# Define the send_cpu_continue function as before
def send_cpu_continue(continue_or_not=True, data = data):
    if continue_or_not:
        message_payload = "Test123"  # Ensure this is defined or available
        global timer_task
        global seconds
        data = bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + message_payload.encode()
        node.send(data)
        time.sleep(0.2)
        timer_task = Timer(seconds, send_cpu_continue)
        timer_task.start()
    else:
        data = bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + bytes([255]) + message_payload.encode()
        node.send(data)
        time.sleep(0.2)
        timer_task.cancel()

# Start sending immediately after setup
seconds = 3  # Make sure this is defined before you start the loop
send_cpu_continue()  # Start sending without waiting for a keypress

def init():
    # Existing setup code
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    # Assuming the frequency should be in Hz and the library expects an integer

    node = sx126x.sx126x(serial_num="/dev/ttyS0", freq=868, addr=0, power=22, rssi=True, air_speed=2400, relay=False)