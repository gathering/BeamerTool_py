import json
import os

import flask
import requests
import requests_oauthlib

from flask import current_app

class OAuthSignIn(object):
    providers = None

    def __init__(self, client_id, client_secret,auth_url,token_url):
        print(auth_url)
        self.auth_url=auth_url
        self.token_url=token_url
        self.client_id = client_id
        self.client_secret = client_secret

    def authorize(self):
        simplelogin = requests_oauthlib.OAuth2Session(
            self.client_id, redirect_uri="http://localhost:5000/callback"
        )

        authorization_url,_ = simplelogin.authorization_url(self.auth_url)
        return authorization_url

    def callback(self):
        authorization_code = (flask.request.args.get("code"))
        data = {'grant_type': 'authorization_code', 'code': authorization_code,
                'redirect_uri': "http://localhost:5000/callback"}
        print("requesting access token")
        access_token_response = requests.post(self.token_url, data=data, verify=False, allow_redirects=True,
                                              auth=(self.client_id, self.client_secret))
        tokens = json.loads(access_token_response.text)
        access_token = tokens['access_token']
        print("access token: " + access_token)
        return access_token


