"""
Main file for Solar Car Telemetry ELIZA Transmitter. 
Connects to Cellular network and sends periodic messages to ELIZA server using the
sendToELIZA script.

IMPORTANT: To test this script, rename this file from "ELIZAmain.py" to "main.py" and place 
it in the root of the Digi XBee LTE module's file system.
"""

import network
import time
import sendToELIZA

print(" +--------------------------------------+")
print(" |   Solar Car Telemetry Transmitter    |")
print(" +--------------------------------------+\n")

# Connect to Cellular network
conn = network.Cellular()
print("- Connecting to Cellular... ", end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")

# Optional: Sync time with network so 'ts' is accurate
# (Most Cellular modules do this automatically, but good to be aware)
print("- Current System Time: {%s}" % time.time()) 
print("- IP Configuration:", conn.ifconfig())

# Start sending periodic messages to ELIZA server
print("\nStarting periodic message sending to ELIZA server...")
sendToELIZA.send_ELIZA_periodic()