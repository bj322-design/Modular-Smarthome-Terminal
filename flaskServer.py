from flask import Flask, render_template

from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def clientHome():
    return render_template("index.html")
@app.route("/settings")
def settings():
    return render_template("settingspage.html")
@app.route("/api/layout", methods=["GET"])
def get_layout():
    with open("layout_client.json", "r") as file:
        layout = json.load(file)

    return jsonify(layout)


@app.route("/api/layout", methods=["POST"])
def save_layout():
    new_layout = request.json

    with open("layout_client.json", "w") as file:
        json.dump(new_layout, file, indent=4)

    return jsonify({"message": "Layout saved"})


@app.route("/api/layout/default", methods=["POST"])
def reset_layout():
    with open("default_layout_client.json", "r") as file:
        default_layout = json.load(file)

    with open("layout_client.json", "w") as file:
        json.dump(default_layout, file, indent=4)

    return jsonify(default_layout)

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)

def thread():
    setup()
    run()

def setup():
    app.run(debug=True)

def run():
    print("Flask server running...")
    time.sleep(5)