from flask import Flask, session, redirect, request, render_template, url_for, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import model

app = Flask(__name__)
app.secret_key="SetSecretKeyHere"
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
    if current_user.is_anonymous:
        return redirect("/static/login.html")
    else:
        return render_template("mainpage.html")

@app.route("/")
def index():
    return redirect("/static/login.html")


@app.route("/load", methods=["GET"])
def load_image():
    auth_data = request.authorization
    user_name = auth_data.username
    password = auth_data.password
    if not model.is_password_valid(user_name, password):
        abort(401)

    drawing_name = request.headers.get("DrawingName")
    pixel_data = model.get_pixel_data(drawing_name, user_name)
    status = "OK"
    if not pixel_data:
        status = "FAILED TO GET PIXEL DATA"

    result = dict(status=status, pixels=pixel_data)
    return jsonify(result)

@app.route("/save", methods=["POST"])
def save_image():
    auth_data = request.authorization
    user_name = auth_data.username
    password = auth_data.password
    if not model.is_password_valid(user_name, password):
        abort(401)

    json_data = request.get_json()
    drawing_name = json_data.get("drawingName")
    pixel_data = json_data.get("drawingData")
    model.save_drawing(drawing_name, user_name, pixel_data)
    return "Save Successful"


@app.route("/usercreds", methods=["GET"])
def get_user_creds():
    user_id = session.get("user_id")
    password = model.get_user(user_id).password
    credentials = {"username": user_id,
                   "password": password}
    return jsonify(credentials)


@app.route("/new")
def new_image():
    return "Stub stuff for server side new image creation..."

if __name__ == '__main__':
    app.run(debug=True)