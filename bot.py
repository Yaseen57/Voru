import subprocess
import signal
import os
import sys
import requests
import tarfile
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ssh_ngrok.log'),
        logging.StreamHandler()
    ]
)

# Constants
NGROK_URL = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
NGROK_TAR = "ngrok-v3-stable-linux-amd64.tgz"
NGROK_DIR = "./ngrok"
NGROK_AUTH_TOKEN = "2ULlZeaFoXx7Kqk7kcYMlsel5JO_3mMWSwcCzs7uL4jtRaQ44"

# Function to download and extract ngrok
def download_and_extract_ngrok():
    try:
        response = requests.get(NGROK_URL)
        with open(NGROK_TAR, 'wb') as file:
            file.write(response.content)
        with tarfile.open(NGROK_TAR, 'r:gz') as tar:
            tar.extractall(path=NGROK_DIR)
        logging.info("Downloaded and extracted ngrok successfully")
    except Exception as e:
        logging.error(f"Failed to download and extract ngrok: {e}")

# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    logging.info("Interrupt received, terminating subprocesses...")
    ssh_process.terminate()
    ngrok_process.terminate()
    ssh_process.wait()
    ngrok_process.wait()
    sys.exit(0)

# Check if the script is run as root
if os.geteuid() != 0:
    logging.error("This script must be run as root")
    sys.exit(1)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Download and extract ngrok
if not os.path.exists(NGROK_DIR):
    os.makedirs(NGROK_DIR)
download_and_extract_ngrok()

# Add ngrok authtoken
try:
    ngrok_auth_command = f"{NGROK_DIR}/ngrok config add-authtoken {NGROK_AUTH_TOKEN}"
    subprocess.run(ngrok_auth_command, shell=True, check=True)
    logging.info("Added ngrok authtoken successfully")
except Exception as e:
    logging.error(f"Failed to add ngrok authtoken: {e}")

# Install and start the SSH server
try:
    install_ssh_command = "apt update && apt install -y openssh-server"
    subprocess.run(install_ssh_command, shell=True, check=True)
    logging.info("Installed and started SSH server successfully")
except Exception as e:
    logging.error(f"Failed to install and start SSH server: {e}")

# Set password for user 'turjaun' and start the SSH service
try:
    ssh_command = "echo 'turjaun:1234' | chpasswd && service ssh start"
    ssh_process = subprocess.Popen(ssh_command, shell=True)
    logging.info("Set password for user 'turjaun' and started SSH service")
except Exception as e:
    logging.error(f"Failed to set password or start SSH service: {e}")

# Start ngrok for SSH
try:
    ngrok_command = f"{NGROK_DIR}/ngrok tcp 22"
    ngrok_process = subprocess.Popen(ngrok_command, shell=True)
    logging.info("Started ngrok for SSH successfully")
except Exception as e:
    logging.error(f"Failed to start ngrok for SSH: {e}")

# Wait for the subprocesses to complete
try:
    ssh_process.wait()
    ngrok_process.wait()
except Exception as e:
    logging.error(f"Error occurred while waiting for subprocesses: {e}")
finally:
    if ssh_process.poll() is None:
        ssh_process.terminate()
    if ngrok_process.poll() is None:
        ngrok_process.terminate()
