#!/usr/bin/env python3
"""
End to end integration Test
"""
import requests


def register_user(email: str, password: str) -> None:
    """User registration test"""
    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/users", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post("http://localhost:5000/users", data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Invalid login test"""
    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/sessions", data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Valid login test"""
    data = {"email": email, "password": password}
    response = requests.post("http://localhost:5000/sessions", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Testing an unlogged profile"""
    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Testing a logged profile"""
    cookies = {"session_id": session_id}
    email = "guillaume@holberton.io"
    response = requests.get("http://localhost:5000/profile", cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"email": email}


def log_out(session_id: str) -> None:
    """User logout test"""
    cookies = {"session_id": session_id}
    url = "http://localhost:5000/sessions"
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Reset password test"""
    data = {"email": email}
    response = requests.post("http://localhost:5000/reset_password", data=data)
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password test"""
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put("http://localhost:5000/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
