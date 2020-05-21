import datetime

import jwt
from flask import request, jsonify, session
from backend import app
from backend.models import User


@app.route('/verify_user', methods=['GET', 'POST'])
def verify_user():
    session.permanent = True
    # username = request.args.get("name")
    username = request.form.get('name')
    # password = request.args.get("password")
    password = request.form.get('password')
    # user = User.query.filter(User.name==username).first()
    user = User.query.filter_by(name=username).first()
    # There is difference between filter and filter by!
    if user == None:
        status = "false"
        return jsonify(status=status)
    else:
        if user.pwd == password:
            session.permanent = True
            app.permanent_session_lifetime = datetime.timedelta(minutes=1)
            time = str(datetime.datetime.now())
            b_token = jwt.encode({"username": username, "time": time}, 'secret', algorithm='HS256')
            session["username"] = username
            session["token"] = b_token.decode("utf-8")
            status = "Successful"
            return jsonify(status=status, username=username, token=b_token.decode("utf-8"))
        else:
            status = "Failed"
            return jsonify(status=status, name=username)


@app.route('/log_out')
def log_out():
    if is_user_authenticated():
        session.clear()
        return jsonify(status="Successful")
    else:
        return jsonify(error_msg="Unauthorized log out!", status="Failed")


def is_user_authenticated():
    frontend_token = request.headers['token']
    session_token = session.get("token")
    print("f", frontend_token)
    print("s", session_token)
    if session_token == frontend_token and session_token != None and frontend_token != None:
        print("Authorized action")
        return True
    else:
        print("Unauthorized action")
        return False


@app.route('/access_control')
def access_control():
    session_token = session.get("token")
    frontend_token = request.args.get("token")
    print(session.get("token"))
    print(session.get("username"))
    print(session_token)
    print(frontend_token)
    if session_token == frontend_token and session_token != None and frontend_token != None:
        print("Verified user is requesting!")
        status = "Successful"
    else:
        print("Unverified user!")
        status = "Failed"
    return jsonify(status=status)
