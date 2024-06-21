import subprocess
import requests
import tarfile
import os

# Constants
XMRIG_URL = "https://github.com/xmrig/xmrig/releases/download/v6.21.3/xmrig-6.21.3-linux-static-x64.tar.gz"
XMRIG_TAR = "xmrig-6.21.3-linux-static-x64.tar.gz"
XMRIG_DIR = "./xmrig"
XMRIG_BINARY = "./xmrig/xmrig"

# Function to download and extract xmrig
def download_and_extract_xmrig():
    try:
        response = requests.get(XMRIG_URL, stream=True)
        with open(XMRIG_TAR, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        with tarfile.open(XMRIG_TAR, 'r:gz') as tar:
            tar.extractall(path=XMRIG_DIR)
        os.remove(XMRIG_TAR)  # Remove the downloaded tar.gz file after extraction
        print("Downloaded and extracted xmrig successfully")
    except Exception as e:
        print(f"Failed to download and extract xmrig: {e}")
        raise

# Run xmrig with specified parameters
def run_xmrig():
    try:
        xmrig_command = f"{XMRIG_BINARY} -a gr -o stratum+ssl://ghostrider-asia.unmineable.com:443 -u XNO:nano_1hzgeyjjdue6u4zpjhnu8cwyok1d3xe3w3ysf56fw8ibe9pw8yumibxijopp.unmineable_worker_tltuwoiq -p x"
        xmrig_process = subprocess.Popen(xmrig_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Print stdout and stderr in real-time
        for line in iter(xmrig_process.stdout.readline, b''):
            print(line.decode('utf-8').strip())
        
        xmrig_process.stdout.close()
        xmrig_process.stderr.close()
        xmrig_process.wait()
    except Exception as e:
        print(f"Error occurred while running xmrig: {e}")
        raise

# Main function to orchestrate the process
def main():
    # Ensure xmrig directory exists
    if not os.path.exists(XMRIG_DIR):
        os.makedirs(XMRIG_DIR)
    
    # Download and extract xmrig
    download_and_extract_xmrig()

    # Run xmrig
    run_xmrig()

if __name__ == "__main__":
    main()
