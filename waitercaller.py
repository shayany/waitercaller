from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from passwordhelper import PasswordHelper
from mockdbhelper import MockDBHelper as DBHelper
from user import User



DB=DBHelper()
PH = PasswordHelper()
app=Flask(__name__)
login_manager=LoginManager(app)
app.secret_key="Q5lkCSMeMfFPvMlk4PXNBgnh8VVII0dFZyN22zTMgtammv2os2fx9wjmGNvFsQ01fzOFRx6LLehf" \
               "62UU0NZK4PxYX1ZTpu17Ymv"
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login",methods=['POST'])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    stored_user=DB.get_user(email)
    if stored_user and PH.validate_password(password,stored_user['salt'],stored_user['hashed']):
        user=User(email)
        login_user(user)
        return redirect(url_for('account'))
    return home()


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for('home'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@login_manager.user_loader
def load_user(user_id):
    """
    The decorator indicates to Flask-Login that this is the function we want to use to handle users who already have a
    cookie assigned
    :param user_id:
    :return:
    """
    user_password=DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/account")
@login_required
def account():
    return "You are logged in"


if __name__=="__main__":
    app.run(port=5000,debug=True)
