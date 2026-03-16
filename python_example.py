import requests
import os
import sys
import subprocess

# --- UPDATED LINKS ---
VERSION_URL = "https://raw.githubusercontent.com/Lexus101987/Update_finder/main/version.txt"
EXE_URL = "https://github.com/Lexus101987/Update_finder/raw/main/dist/python_example.exe"

VERSION = "2" 
FILENAME = sys.argv[0] 

def check_and_update():
    print(f"Checking for updates... (Local: v{VERSION})")
    try:
        v_response = requests.get(VERSION_URL)
        if v_response.status_code == 200:
            online_version = v_response.text.strip()
            
            if online_version == VERSION:
                print("No updates found.")
                return
            
            print(f"New version v{online_version} detected! Downloading...")
            
            r = requests.get(EXE_URL, stream=True)
            if r.status_code == 200:
                with open("temp_update.exe", "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Verify file size to ensure it's not a 0kb empty file
                if os.path.exists("temp_update.exe") and os.path.getsize("temp_update.exe") > 0:
                    print("Download successful. Swapping files...")
                    
                    with open("updater.bat", "w") as f:
                        f.write(f"""
@echo off
timeout /t 2 /nobreak > nul
del /f /q "{FILENAME}"
move /y "temp_update.exe" "{FILENAME}"
start "" "{FILENAME}"
del "%~f0"
""")
                    subprocess.Popen(["updater.bat"], shell=True)
                    os._exit(0) # Immediate shutdown
                else:
                    print("Error: Downloaded file is empty or missing.")
            else:
                print(f"Failed to download EXE. GitHub Status: {r.status_code}")
    except Exception as e:
        print(f"Update error: {e}")

if __name__ == "__main__":
    # Only check for updates if we are running as an EXE
    if FILENAME.endswith(".exe"):
        check_and_update()
    
    print(f"--- App v{VERSION} is now running ---")
    input("\nPress Enter to exit...")