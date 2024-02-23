#!/usr/bin/env python3
"""Flask app instance"""
from flask import [Flask, jsonify, request, abort,
                   make_response, url_for, redirect]
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """Index route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Users route"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password:
        try:
            new_user = AUTH.register_user(email, password)
            return jsonify({"email": email, "message": "user created"})

        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """User login"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = make_response(jsonify({"email": email,
                                     "message": "logged in"}))
            response.set_cookie("session_id", session_id)
            return response
        else:
            abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """User logout"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect(url_for("index"))
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
