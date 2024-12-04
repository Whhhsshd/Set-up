import os
import subprocess
import time
import hashlib
import requests

def clear_history():
    subprocess.run("history -c", shell=True)

def ask_telegram_token():
    token = input("Enter your Telegram bot token: ")
    return token

def generate_device_id():
    # Get Termux info (assuming termux-info is installed)
    try:
        termux_info = subprocess.check_output("termux-info", shell=True).decode("utf-8")
        # Extract relevant data from termux-info (for uniqueness)
        unique_info = termux_info.splitlines()[0]  # Just using first line for simplicity, you can choose others
        # Create a hash of the information to generate a unique device ID
        device_id = hashlib.sha256(unique_info.encode('utf-8')).hexdigest()[:16]  # Limit to 16 characters for simplicity
        return device_id
    except subprocess.CalledProcessError:
        print("Error generating device ID. Please ensure `termux-tools` is installed.")
        exit(1)

def check_device_approval(device_id):
    # Replace with the URL where device IDs are checked
    url = "http://twstos.infinityfreeapp.com/device_manager.php"
    params = {'deviceid': device_id}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.text
            if "approved" in data:
                return True
            elif "expired" in data:
                print("Your device has expired. Please contact admin.")
            else:
                print(f"Your device {device_id} is pending approval. Please contact admin.")
        else:
            print(f"Error: Unable to check device status. Server returned status code {response.status_code}")
    except requests.exceptions.RequestException:
        print("Error contacting server. Please try again later.")
    return False

def local_setup():
    print("Select key type: 1. Free 2. Paid")
    key_type = input("Enter 1 or 2: ")

    if key_type == "1":  # Free setup
        print("Cloning FREE repository...")
        subprocess.run("git clone https://github.com/Whhhsshd/FREE.git", shell=True)
        subprocess.run("cd FREE", shell=True)
        token = ask_telegram_token()
        
        # Generate device ID from Termux
        device_id = generate_device_id()
        
        # Check device approval
        if not check_device_approval(device_id):
            print(f"Your device {device_id} is pending approval.")
            input("Press Enter to try again after approval.")
            return  # Exit and wait for approval

        # Save token and device ID in the cloned directory
        with open("FREE/token.txt", "w") as token_file:
            token_file.write(token)
        
        with open("FREE/device_id.txt", "w") as device_id_file:
            device_id_file.write(device_id)
        
        subprocess.run(f"nohup python3 FREE/bot.py &", shell=True)
        print("Bot is running in the background.")
        time.sleep(1)
        clear_history()

    elif key_type == "2":  # Paid setup
        print("Cloning PAID repository...")
        subprocess.run("git clone https://github.com/Whhhsshd/PAID.git", shell=True)
        subprocess.run("cd PAID", shell=True)
        token = ask_telegram_token()
        
        # Generate device ID from Termux
        device_id = generate_device_id()
        
        # Check device approval
        if not check_device_approval(device_id):
            print(f"Your device {device_id} is pending approval.")
            input("Press Enter to try again after approval.")
            return  # Exit and wait for approval
        
        # Save token and device ID in the cloned directory
        with open("PAID/token.txt", "w") as token_file:
            token_file.write(token)
        
        with open("PAID/device_id.txt", "w") as device_id_file:
            device_id_file.write(device_id)
        
        subprocess.run(f"nohup python3 PAID/bot.py &", shell=True)
        print("Bot is running in the background.")
        time.sleep(1)
        clear_history()

def cloud_server_setup():
    vps_ip = input("Enter your VPS IP: ")
    vps_user = input("Enter your VPS username: ")
    vps_pass = input("Enter your VPS password: ")

    print(f"Connecting to {vps_ip} on port 22...")
    # Use SSH to connect to the VPS and run the same commands
    ssh_command = f"sshpass -p '{vps_pass}' ssh {vps_user}@{vps_ip} 'git clone https://github.com/Whhhsshd/FREE.git; cd FREE; nohup python3 FREE/bot.py &'"
    subprocess.run(ssh_command, shell=True)
    
    # Generate device ID from Termux
    device_id = generate_device_id()
    
    # Check device approval
    if not check_device_approval(device_id):
        print(f"Your device {device_id} is pending approval.")
        input("Press Enter to try again after approval.")
        return  # Exit and wait for approval
    
    # Save token and device ID in the cloned directory on VPS
    ssh_command = f"sshpass -p '{vps_pass}' ssh {vps_user}@{vps_ip} 'echo \"{device_id}\" > FREE/device_id.txt; echo \"{device_id}\" > PAID/device_id.txt'"
    subprocess.run(ssh_command, shell=True)
    
    print("Bot is running in the background on your VPS.")
    time.sleep(1)
    clear_history()

def main():
    print("Where would you like to use the bot?")
    print("1. Local setup")
    print("2. Virtual Cloud Server")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        local_setup()
    elif choice == "2":
        cloud_server_setup()
    else:
        print("Invalid choice. Exiting.")
        exit(1)

if __name__ == "__main__":
    main()
