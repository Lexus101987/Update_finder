import requests
import os
import sys
import subprocess

# Points to the EXE on GitHub, not the .py
EXE_URL = "https://github.com/Lexus101987/Update_finder/raw/main/python_example.exe"
VERSION = "2"
FILENAME = sys.argv[0]

def check_and_update():
    print(f"Checking for updates... (Local: v{VERSION})")
    try:
        # In a real app, you'd check a version.txt here first
        response = requests.get(EXE_URL, stream=True)
        
        if response.status_code == 200:
            print("New version detected! Downloading binary update...")
            
            # Use "wb" for Write-Binary
            with open("temp_update.exe", "wb") as f:
                f.write(response.content)
            
            # Create the Batch "Sidekick" to swap the files
            with open("updater.bat", "w") as f:
                f.write(f"""
@echo off
timeout /t 2 /nobreak > nul
del "{FILENAME}"
move /y "temp_update.exe" "{FILENAME}"
start "" "{FILENAME}"
del "%~f0"
""")
            
            print("Update downloaded. Restarting...")
            subprocess.Popen(["updater.bat"], shell=True)
            sys.exit() # Close the current app so the .bat can delete it
            
    except Exception as e:
        print(f"Update error: {e}")