from flask import Flask


app = Flask(__name__)

@app.route("/")
def clientHome():
    return "<center><h1>Hello This is the placeholder for the <b>index.html</b></h1></center>" #render_template("clientHome.html")


if __name__ == '__main__':
    app.run(debug=True)
