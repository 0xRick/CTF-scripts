#!/usr/bin/env python
import ses
from flask import session,redirect, url_for, request,render_template, jsonify,Flask, send_from_directory
from threading import Lock
import hashlib
import hmac
import os
import base64
import subprocess
import time

def get_secure_key():
    m = hashlib.sha1()
    m.update(os.urandom(32))
    return m.hexdigest()

def craft_secure_token(content):
    h = hmac.new("HMACSecureKey123!", base64.b64encode(content).encode(), hashlib.sha256)
    return h.hexdigest()


lock = Lock()
app = Flask(__name__)
app.config['SECRET_KEY'] = get_secure_key()
Managers = {}

def log_creds(ip, c):
    with open("creds.log", "a") as creds:
        creds.write("Login from {} with data {}:{}\n".format(ip, c["username"], c["password"]))
        creds.close()

def safe_get_manager(id):
    lock.acquire()
    manager = Managers[id]
    lock.release()
    return manager

def safe_init_manager(id):
    lock.acquire()
    if id in Managers:
        del Managers[id]
    else:
            login = ["<REDACTED>", "<REDACTED>"]
            Managers.update({id: ses.SessionManager(login, craft_secure_token(":".join(login)))})
    lock.release()

def safe_have_manager(id):
    ret = False
    lock.acquire()
    ret = id in Managers
    lock.release()
    return ret

@app.before_request
def before_request():
    if request.path == "/":
        if not session.has_key("id"):
            k = get_secure_key()
            safe_init_manager(k)
            session["id"] = k
        elif session.has_key("id") and not safe_have_manager(session["id"]):
            del session["id"]
            return redirect("/", 302)
    else:
        if session.has_key("id") and safe_have_manager(session["id"]):
            pass
        else:
            return redirect("/", 302)

@app.after_request
def after_request(resp):
    return resp


@app.route('/assets/<path:filename>')
def base_static(filename):
    return send_from_directory(app.root_path + '/assets/', filename)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET'])
def view_login():
    return render_template("login.html")

@app.route('/auth', methods=['POST'])
def login():
    ret = {"authenticated": None, "result": None}
    manager = safe_get_manager(session["id"])
    data = request.get_json(silent=True)
    if data:
        try:
            tmp_login = dict(data["data"])
        except:
            pass
        tmp_user_login = None
        try:
            is_logged = manager.check_login(data)
            secret_token_info = ["/api/<api_key>/job", manager.secret_key, int(time.time())]
            try:
                tmp_user_login = {"username": tmp_login["username"], "password": tmp_login["password"]}
            except:
                pass
            if not is_logged[0]:
                ret["authenticated"] = False
                ret["result"] = "Cannot authenticate with data: %s - %s" % (is_logged[1], "Too many tentatives, wait 2 minutes!" if manager.blocked else "Try again!")
            else:
                if tmp_user_login is not None:
                    log_creds(request.remote_addr, tmp_user_login)
                ret["authenticated"] = True
                ret["result"] = {"endpoint": secret_token_info[0], "key": secret_token_info[1], "creation_date": secret_token_info[2]}
        except TypeError as e:
            ret["authenticated"] = False
            ret["result"] = str(e)
    else:
        ret["authenticated"] = False
        ret["result"] = "Cannot authenticate missing parameters."
    return jsonify(ret)


@app.route("/api/<key>/job", methods=['POST'])
def job(key):
    ret = {"success": None, "result": None}
    manager = safe_get_manager(session["id"])
    if manager.secret_key == key:
        data = request.get_json(silent=True)
        if data and type(data) == dict:
            if "schedule" in data:
                out = subprocess.check_output(['bash', '-c', data["schedule"]])
                ret["success"] = True
                ret["result"] = out
            else:
                ret["success"] = False
                ret["result"] = "Missing schedule parameter."
        else:
            ret["success"] = False
            ret["result"] = "Invalid value provided."
    else:
        ret["success"] = False
        ret["result"] = "Invalid token."
    return jsonify(ret)


app.run(host='127.0.0.1', port=5000)
