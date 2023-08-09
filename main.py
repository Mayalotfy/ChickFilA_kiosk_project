from flask import Flask, session, abort, redirect, request,render_template,send_from_directory
from datetime import datetime

#import files
import kiosk
import manager
import server
from app import *

#login infos
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app.secret_key = "CodeSpecialist.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "483069400399-ouhtkda4i1ag9vvj1nc8d8todscrrrpl.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    #redirect_uri = "http://127.0.0.1:5000/callback1" # locally
    redirect_uri = "https://chickfillaiota.herokuapp.com/callback1"  # render
)

def get_timestamp():
    """
    Returns the current timestamp as a formatted string.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_todaydate():
    """
    Returns the current date as a formatted string.
    """
    current_date = datetime.now()
    return current_date.strftime("%Y%m%d")


@app.route('/')
def index():
    """
    Renders the main page of the website.
    """
    session.clear()
    timestamp = get_timestamp()
    return render_template('Connect_all/main.html',timestamp=timestamp)

@app.route('/kiosk')
def kiosk():
    """
    Renders the kiosk page of the website and clears the session.
    """
    session.clear()
    return render_template('kiosk/kiosk.html')

@app.route("/managerlogin")
def managerlogin():
    """
    Redirects the user to the Google OAuth2 authorization URL for manager access.
    """
    flow.redirect_uri = "https://chickfillaiota.herokuapp.com/callback1"
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/serverlogin')
def serverlogin():
    """
    Redirects the user to the Google OAuth2 authorization URL for server access.
    """
    flow.redirect_uri = "https://chickfillaiota.herokuapp.com/callback2"
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/map")
def map():
    """
    Renders the map page of the website.
    """
    lat = 30.61213892669398
    lng = -96.3414524265124
    return render_template('Connect_all/map.html', code_lat=lat, code_lng=lng)

@app.route("/callback1")
def callback1():
    """
    Fetches the OAuth2 token for manager access and verifies the Google ID token.
    """
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/manager")

@app.route("/callback2")
def callback2():
    """
    Fetches the OAuth2 token for server access and verifies the Google ID token.
    """
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/server")

@app.route("/logout")
@Summary.login_is_required
def logout():
    """
    Clears the session and logs the user out of the website.
    """
    session.clear()
    for key in list(session.keys()):
         session.pop(key)
    return redirect("/")

# Add a route to serve the generated documentation HTML file
@app.route('/pydocs/<path:path>')
def serve_docs(path):
    return send_from_directory('pydocs', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

