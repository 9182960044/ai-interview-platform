from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

app.config["SECRET_KEY"] = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///interview.db"


db = SQLAlchemy(app)


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# ===========================
# DATABASE
# ===========================
class User(
    UserMixin,
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(200)
    )


@login_manager.user_loader
def load_user(
    user_id
):

    return User.query.get(
        int(user_id)
    )


# ===========================
# HOME
# ===========================
@app.route("/")
@login_required
def home():

    return render_template(
        "index.html",
        questions=None
    )


# ===========================
# REGISTER
# ===========================
@app.route(
    "/register",
    methods=[
        "GET",
        "POST"
    ]
)
def register():

    if request.method == "POST":

        user = User(

            username=request.form["username"],

            email=request.form["email"],

            password=generate_password_hash(
                request.form["password"]
            )

        )

        db.session.add(
            user
        )

        db.session.commit()

        return redirect(
            "/login"
        )

    return render_template(
        "register.html"
    )


# ===========================
# LOGIN
# ===========================
@app.route(
    "/login",
    methods=[
        "GET",
        "POST"
    ]
)
def login():

    if request.method == "POST":

        user = User.query.filter_by(

            email=request.form["email"]

        ).first()

        if user and check_password_hash(

            user.password,

            request.form["password"]

        ):

            login_user(
                user
            )

            return redirect("/")

    return render_template(
        "login.html"
    )


# ===========================
# LOGOUT
# ===========================
@app.route("/logout")
def logout():

    logout_user()

    return redirect(
        "/login"
    )


# ===========================
# RUN
# ===========================
if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(
        debug=True
    )