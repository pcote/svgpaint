from flask import Flask, redirect, request, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import model


app = Flask(__name__)
logman = LoginManager()
logman.init_app(app)

@logman.user_loader
def load_user(user_id):
    user = model.get_user(user_id)
    return user

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("usernameTF")
    password = request.form.get("passwordTF")
    password_correct = model.is_password_valid(username, password)

    if password_correct:
        user = model.get_user(username)
        user.is_active = True
        user.is_authenticated = True
        login_user(user)
        return redirect(url_for("main_page"))
    else:
        return "Your credentials are wrong. Please backspace and try again"


@app.route("/logout")
def logout():
    username = current_user.username
    model.set_authenticate(username, False)
    logout_user()
    return redirect("/static/login.html")


@app.route("/mainpage")
def main_page():
    return render_template("mainpage.html")


@app.route("/")
def index():
    return redirect("/static/login.html")


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
    app.secret_key="SetSecretKeyHere"
    app.run(debug=True)