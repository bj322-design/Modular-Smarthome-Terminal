from flask import Flask, render_template
from clock_widget import clockWidget

from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route("/time")
def get_time():
    clock = clockWidget()
    current_time = clock.update()
    return jsonify({"time": current_time})

@app.route("/")
def clientHome():
    clock = clockWidget()
    current_time = clock.update()
    return render_template("index.html", time=current_time)

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)

# def thread():
#     setup()

# def setup():
#     app.run(debug=True)