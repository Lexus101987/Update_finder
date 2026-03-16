import requests
import os
import sys
import subprocess
import time

# --- CONFIGURATION ---
# Use the DIRECT RAW links from GitHub
VERSION_URL = "https://raw.githubusercontent.com/Lexus101987/Update_finder/main/version.txt"
EXE_URL = "https://github.com/Lexus101987/Update_finder/raw/main/python_example.exe"

VERSION = "1" # Current version of THIS file
FILENAME = sys.argv[0] # This will be 'python_example.exe' when compiled

def check_and_update():
    print(f"Checking for updates... (Local: v{VERSION})")
    try:
        # 1. Check the version file first to see if we need an update
        v_response = requests.get(VERSION_URL)
        if v_response.status_code == 200:
            online_version = v_response.text.strip()
            
            if online_version == VERSION:
                print("No updates found. You are on the latest version.")
                return
            
            print(f"New version v{online_version} detected! Downloading...")
            
            # 2. Download the NEW EXE as a binary file
            # Use 'stream=True' for larger files
            r = requests.get(EXE_URL, stream=True)
            if r.status_code == 200:
                with open("temp_update.exe", "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print("Download complete. Preparing to swap files...")
                
                # 3. Create a Batch file to handle the file swap
                # This script waits 2 seconds, deletes the old EXE, 
                # renames the new one, starts it, and deletes itself.
                with open("updater.bat", "w") as f:
                    f.write(f"""
@echo off
timeout /t 2 /nobreak > nul
del /f /q "{FILENAME}"
move /y "temp_update.exe" "{FILENAME}"
start "" "{FILENAME}"
del "%~f0"
""")
                
                print("Restarting app to apply update...")
                # Run the batch file in the background
                subprocess.Popen(["updater.bat"], shell=True)
                # Close this app immediately so the .bat can delete the file
                sys.exit()
                
        else:
            print(f"Could not check version (Status: {v_response.status_code})")

    except Exception as e:
        print(f"Update error: {e}")

if __name__ == "__main__":
    # If you are running as a .py file, just run the app. 
    # Auto-updating works best when compiled to an .exe.
    if FILENAME.endswith(".exe"):
        check_and_update()
    else:
        print("Running in Script Mode (Auto-update skipped to avoid overwriting source).")

    print(f"--- App v{VERSION} is now running ---")
    
    # Keep console open so you can see the output
    input("\nPress Enter to exit...")