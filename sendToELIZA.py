"""
Digi XBee LTE ELIZA TCP client.

Sends "Hello World!" every five seconds and appends server responses to the
module file system.
"""

import network
import usocket as socket
import time

# Configuration constants defining ELIZA server address and port, plus message and timing parmeters
SERVER_ADDRESS = "52.43.121.77"
SERVER_PORT = 0x2328  # 9000
MESSAGE = b"Hello World!"
LOG_FILE = "ELIZAlog.txt"
PERIOD_SECONDS = 5
RECEIVE_TIMEOUT_SECONDS = 30

# Logs responses from the server to ELIZAlog.txt
def log_response(data):
	"""Append a timestamped server response to the log file."""
	if not data:
		return

	try:
		response = data.decode("utf-8")
	except Exception:
		response = repr(data)

	with open(LOG_FILE, "a") as log:
		log.write("{}: {}\n".format(time.time(), response))

# Function for ELIZAmain.py, Sends periodic messages to the ELIZA server and logs responses
def send_ELIZA_periodic():
	while True:
		sock = None
		try:
			# A new connection is used for each message so the script can
			# recover cleanly if the cellular connection is interrupted.
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(RECEIVE_TIMEOUT_SECONDS)
			sock.connect((SERVER_ADDRESS, SERVER_PORT))
			sock.send(MESSAGE)

			while True:
				try:
					response = sock.recv(1024)
					if not response:
						break
					print("Received response: %s" % response.decode('utf-8'))
					log_response(response)
				except OSError as timeout_error:
					print("No response received from the server. Socket timed out")
					with open(LOG_FILE, "a") as log:
						log.write("%s: ERROR: %s\n" % (time.time(), timeout_error))
					break
		except Exception as error:
			with open(LOG_FILE, "a") as log:
				log.write("%s: ERROR: %s\n" % (time.time(), error))
			print("Error occurred while sending message: %s" % error)
		finally:
			# Close the socket to free up resources
			if sock is not None:
				try:
					sock.close()
				except Exception:
					pass

		# Wait for the specified period before sending the next message
		time.sleep(PERIOD_SECONDS)

# Function for manual sendToELIZA call, same as send_ELIZA_periodic but connects to cellular network before sending
def manualSendPeriodic():

	print(" +--------------------------------------+")
	print(" |   Solar Car Telemetry Transmitter    |")
	print(" +--------------------------------------+\n")

	conn = network.Cellular()
	print("- Connecting to Cellular... ", end="")
	while not conn.isconnected():
		time.sleep(5)
	print("[OK]")

	# Optional: Sync time with network so 'ts' is accurate
	# (Most Cellular modules do this automatically, but good to be aware)
	print("- Current System Time: {%s}" % time.time()) 
	print("- IP Configuration:", conn.ifconfig())

	while True:
		sock = None
		try:
			# A new connection is used for each message so the script can
			# recover cleanly if the cellular connection is interrupted.
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(RECEIVE_TIMEOUT_SECONDS)
			sock.connect((SERVER_ADDRESS, SERVER_PORT))
			sock.send(MESSAGE)

			while True:
				try:
					response = sock.recv(1024)
					if not response:
						break
					print("Received response: %s" % response.decode('utf-8'))
					log_response(response)
				except OSError as timeout_error:
					print("No response received from the server. Socket timed out")
					with open(LOG_FILE, "a") as log:
						log.write("%s: ERROR: %s\n" % (time.time(), timeout_error))
					break
		except Exception as error:
			print("Error occurred while sending message: %s" % error)
			with open(LOG_FILE, "a") as log:
				log.write("%s: ERROR: %s\n" % (time.time(), error))
		finally:
			# Close the socket to free up resources
			if sock is not None:
				try:
					sock.close()
				except Exception:
					pass

		# Wait for the specified period before sending the next message
		time.sleep(PERIOD_SECONDS)

# If this script is run directly, call the manualSendPeriodic function to connect to cellular network and start sending messages
manualSendPeriodic()

