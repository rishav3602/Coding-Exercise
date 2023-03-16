import socket
import logging

# Configuration
host = ""  # Accept connections from any host
port = 1234  # Change this if you want to use a different port

# Set up logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    filename="app_b.log",
)

# Create a socket for listening to incoming connections
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    logging.info("In the try block")
    sock.bind((socket.gethostname(), port))
    sock.listen()
    logging.info("Trying to establish connection")
except socket.error:
    logging.exception("Failed to bind to the socket.")
    raise

# Main loop
while True:
    # Wait for a connection
    try:
        logging.info("In the main loop")
        conn, addr = sock.accept()
        logging.info("connection established")
        print ("connection established")
    except socket.error:
        logging.exception("Failed to accept a connection.")
        raise

    # Read messages from the connection and display them
    while True:
        try:
            logging.info("In the sub loop")
            data = conn.recv(1024)
        except socket.error:
            logging.exception("Failed to receive data.")
            raise

        if not data:
            logging.info("Trying to execute if block")
            break
        logging.info("Trying to print the message")
        message = data.decode().strip()
        print(message)  # Change this to your code for displaying the message
        logging.info(message)

    conn.close()
