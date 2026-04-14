from flask import Flask, render_template
from flask import Flask
from flask import jsonify

from SMTplugins.pluginImports import *


app = Flask(__name__)



#######PLUGINS#######
app.register_blueprint(clock_bp)
app.register_blueprint(fTemp_bp)






#allows for easier starting of flask from start file
def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)



@app.route("/")
def clientHome():
    return render_template("index.html")
  
@app.route("/settings")
def settings():
    return render_template("settingspage.html")

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)
