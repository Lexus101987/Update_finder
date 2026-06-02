from flask import Flask
import threading
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running online 24/7!"

def my_background_task():
    while True:
        print("⏰ Script is active and working in the background...")
        # Put your actual automation or bot code here later!
        time.sleep(60)

if __name__ == "__main__":
    # This runs your background code on a separate thread so it doesn't block the web page
    threading.Thread(target=my_background_task, daemon=True).start()
    
    # This tells Flask to listen to the port Render gives us
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)