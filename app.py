from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def index():
    # Add a 5-minute delay
    time.sleep(300)
    return "<h1>Hello Azure! After 5 minutes</h1>"

if __name__ == "__main__":
    app.run()
