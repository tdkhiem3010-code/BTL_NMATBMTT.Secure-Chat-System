import os
import sys
from flask import session

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(
    BASE_DIR
)
from flask import Flask
from flask_socketio import SocketIO
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from websocket.socket_handler import (
    register_socket_events
)

from auth.user_manager import (
    register_user,
    login_user
)

app = Flask(__name__)
socketio = SocketIO(
    app,
    async_mode="threading",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)
register_socket_events(
    socketio
)
app.secret_key = "secure_chat_secret_key"


@app.route(
    "/",
    methods=[
        "GET",
        "POST"
    ]
)
def home():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        success = login_user(
            username,
            password
        )

        if success:

            session["username"] = username

            return redirect(
                "/chat"
            )

        return "Invalid username or password"

    return render_template(
        "login.html"
    )


@app.route(
    "/register",
    methods=[
        "GET",
        "POST"
    ]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )

        success = register_user(
            username,
            password
        )

        if success:

            return redirect(
                "/"
            )

        return "Username already exists"

    return render_template(
        "register.html"
    )


@app.route("/chat")
def chat():

    if "username" not in session:

        return redirect(
            "/"
        )

    return render_template(
        "chat.html",
        username=session["username"],
        current_user=session["username"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        "/"
    )


@app.route("/debug")
def debug_state():
    from websocket.socket_handler import user_sids, online_users
    return {
        "user_sids": user_sids,
        "online_users": online_users
    }


if __name__ == "__main__":

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )