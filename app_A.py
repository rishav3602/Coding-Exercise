##  my client

import os
import time
import socket
import logging

# Configuration
file_name = "test.txt"  # Change this to your file's name
host = ""  # Change this if you want to connect to a different host
port = 1234  # Change this if you want to use a different port

# Set up logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    filename="app_a.log",
)

# Create a socket for sending messages
logging.info("Creating a connection function")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.info("Trying to establish connection")
sock.connect((socket.gethostname(), port))
logging.info("connection established")
print("Welcome to the client")
message = sock.recv(1024)

# Track the last modification time of the file
try:
    logging.info("In the first try block")
    last_modification_time = os.path.getmtime(file_name)
except OSError:
    logging.exception("Failed to get the last modification time of the file.")
    raise

# Main loop
while True:
    # Check if the file has been modified
    try:
        modification_time = os.path.getmtime(file_name)
        
    except OSError:
        logging.exception("Failed to get the modification time of the file.")
        raise

    if modification_time != last_modification_time:
        # Open the file and read its contents
        try:
            with open(file_name) as f:
                lines = f.readlines()
        except OSError:
            logging.exception("Failed to read the file.")
            raise

        # Compare the old and new contents to detect changes
        old_lines = [line.strip() for line in lines]
        new_lines = []
        for i, line in enumerate(lines):
            logging.info("trying to check the file")
            new_lines.append(line.strip())
            if i < len(old_lines) and old_lines[i] != new_lines[i]:
                message = f"Line no:{i+1} is modified from “{old_lines[i]}” to “{new_lines[i]}”."
                try:
                    sock.sendall(message.encode())
                except socket.error:
                    logging.exception("Failed to send a message.")
                    raise
                logging.info(message)
        for i in range(len(old_lines), len(new_lines)):
            message = f"Line no:{i+1} is added “{new_lines[i]}”."
            try:
                logging.info("trying to send message")
                sock.sendall(message.encode())
            except socket.error:
                logging.exception("Failed to send a message.")
                raise
            logging.info(message)
        for i in range(len(new_lines), len(old_lines)):
            message = f"Line no:{i+1} is deleted."
            try:
                sock.sendall(message.encode())
            except socket.error:
                logging.exception("Failed to send a message.")
                raise
            logging.info(message)

        # Update the last modification time
        last_modification_time = modification_time

    # Wait for a short time before checking again
    time.sleep(0.2)
