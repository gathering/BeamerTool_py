import json
import flask
import requests_oauthlib
import os
import requests

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

AUTHORIZATION_BASE_URL = os.environ.get("AUTH_URL")
TOKEN_URL = os.environ.get("TOKEN_URL")
API_BASE = os.environ.get("API_BASE_URL")

# This allows us to use a plain HTTP callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = flask.Flask(__name__)


@app.route("/")
def index():
    return """
    <a href="/login">Login with SimpleLogin</a>
    """


@app.route("/login")
def login():
    simplelogin = requests_oauthlib.OAuth2Session(
        CLIENT_ID, redirect_uri="http://localhost:5000/callback"
    )
    authorization_url, _ = simplelogin.authorization_url(AUTHORIZATION_BASE_URL)
    print(authorization_url)
    return flask.redirect(authorization_url)


@app.route("/callback")
def callback():
    authorization_code=(flask.request.args.get("code"))
    data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': "http://localhost:5000/callback"}
    print("requesting access token")
    access_token_response = requests.post(TOKEN_URL, data=data, verify=False, allow_redirects=True,
                                          auth=(CLIENT_ID, CLIENT_SECRET))

    print(access_token_response)
    print("response")
    print(access_token_response.headers)
    print('body: ' + access_token_response.text)

    # we can now use the access_token as much as we want to access protected resources.
    tokens = json.loads(access_token_response.text)
    access_token = tokens['access_token']
    print("access token: " + access_token)

    api_call_headers = {'Authorization': 'Bearer ' + access_token}
    api_call_response = requests.get(API_BASE+"api/competitions/", headers=api_call_headers, verify=False)
    return f"""
    {data}</br>
    {access_token_response.request.url}</br>
    {access_token_response.headers.values()}</br>
    {access_token}</br>
    <div>{api_call_response.text}</div>
    """



if __name__ == "__main__":
    app.run(debug=True)