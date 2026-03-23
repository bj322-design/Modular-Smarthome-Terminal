from flask import Flask, render_template

from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def clientHome():
    return render_template("index.html")

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)

def thread():
    setup()

def setup():
    app.run(debug=True)