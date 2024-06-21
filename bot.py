import subprocess
import signal
import os
import sys
import requests
import tarfile

# Constants
NGROK_URL = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
NGROK_TAR = "ngrok-v3-stable-linux-amd64.tgz"
NGROK_DIR = "./ngrok"
NGROK_AUTH_TOKEN = "2ULlZeaFoXx7Kqk7kcYMlsel5JO_3mMWSwcCzs7uL4jtRaQ44"

# Function to download and extract ngrok
def download_and_extract_ngrok():
    response = requests.get(NGROK_URL)
    with open(NGROK_TAR, 'wb') as file:
        file.write(response.content)
    with tarfile.open(NGROK_TAR, 'r:gz') as tar:
        tar.extractall(path=NGROK_DIR)

# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("Interrupt received, terminating subprocesses...")
    if ssh_process.poll() is None:
        ssh_process.terminate()
    if ngrok_process.poll() is None:
        ngrok_process.terminate()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Download and extract ngrok
if not os.path.exists(NGROK_DIR):
    os.makedirs(NGROK_DIR)
download_and_extract_ngrok()

# Add ngrok authtoken
ngrok_auth_command = f"{NGROK_DIR}/ngrok config add-authtoken {NGROK_AUTH_TOKEN}"
subprocess.run(ngrok_auth_command, shell=True, check=True)

# Install and start the SSH server
install_ssh_command = "sudo apt update && sudo apt install -y openssh-server"
subprocess.run(install_ssh_command, shell=True, check=True)

# Set password for user 'turjaun' and start the SSH service
ssh_command = "echo 'turjaun:1234' | sudo chpasswd && sudo service ssh start"
ssh_process = subprocess.Popen(ssh_command, shell=True)

# Start ngrok for SSH
ngrok_command = f"{NGROK_DIR}/ngrok tcp 22"
ngrok_process = subprocess.Popen(ngrok_command, shell=True)

# Wait for the subprocesses to complete
try:
    ssh_process.wait()
    ngrok_process.wait()
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    if ssh_process.poll() is None:
        ssh_process.terminate()
    if ngrok_process.poll() is None:
        ngrok_process.terminate()
