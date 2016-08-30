from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/static/index.html")


@app.route("/load", methods=["POST"])
def load_image():
    return "stub for load image server code"

@app.route("/save", methods=["POST"])
def save_image():
    return "Stub code for save image server code...."

@app.route("/new")
def new_image():
    return "Stub stuff for server side new image creation..."

if __name__ == '__main__':
    app.run(debug=True)