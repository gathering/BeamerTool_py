import json

import requests
from flask import Flask, redirect, url_for, render_template, request
import os
import dotenv
from src.unicorn_api.OAuth import OAuthSignIn



app = Flask(__name__)
dotenv.load_dotenv()
client_secret = os.environ.get('CLIENT_SECRET')
client_id = os.environ.get('CLIENT_ID')
auth_url= os.environ.get('AUTH_URL')
print(auth_url)
token_url=os.environ.get("TOKEN_URL")
with app.app_context():
    oauth = OAuthSignIn(client_id, client_secret, auth_url, token_url)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/login/')
def oauth_authorize():
    authorizeurl=oauth.authorize()
    print(authorizeurl)
    return redirect(authorizeurl)


@app.route('/callback/')
def oauth_callback():
    global access
    access = oauth.callback()

    return render_template("return.html",access_token=access)
@app.route('/testapi/')
def testapi():
    api=request.args.get('apiurl')
    api_call_headers = {'Authorization': 'Bearer ' + access}
    api_call_response = requests.get(api, headers=api_call_headers,
                                     verify=False)

    jsondata=json.loads(api_call_response.text)


    return render_template('testapi.html', compodata=jsondata)


if __name__ == '__main__':

    app.run()