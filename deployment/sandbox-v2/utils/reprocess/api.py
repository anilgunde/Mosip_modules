import datetime as dt
import requests
import json
import base64
import os
import secrets
import sys
sys.path.insert(0, '../')
from utils import *

class MosipSession:
    def __init__(self, server, user, pwd, appid='admin', ssl_verify=True, client_token=False):
        self.server = server
        self.user = user
        self.pwd = pwd
        self.ssl_verify = ssl_verify
        if client_token:
            self.token = self.auth_get_client_token(appid, self.user, self.pwd) 
        else:
            self.token = self.auth_get_token(appid, self.user, self.pwd) 
      
    def auth_get_token(self, appid, username, pwd):
        url = '%s/v1/authmanager/authenticate/useridPwd' % self.server
        ts = get_timestamp()
        j = {
            "id": "mosip.io.userId.pwd",
            "metadata" : {},
                "version":"1.0",
                "requesttime": ts,
                "request": {
                    "appId" : appid,
                    "userName": username,
                    "password": pwd
            }
        }
        r = requests.post(url, json = j, verify=self.ssl_verify)
        token = read_token(r)
        return token

    def auth_get_client_token(self, appid, client_id, pwd):
        url = '%s/v1/authmanager/authenticate/clientidsecretkey' % self.server
        ts = get_timestamp()
        j = {
            'id': 'string',
            'metadata': {},
            'request': {
                'appId': appid,
                'clientId': client_id,
                'secretKey': pwd
            },
            'requesttime': ts,
            'version': '1.0'
        }

        r = requests.post(url, json = j, verify=self.ssl_verify)
        token = read_token(r)
        return token

    def notify_securezone(self, registration):
        '''
        policies: dict with policies structure
        '''
        url = '%s/registrationprocessor/v1/securezone/notification' % self.server

        cookies = {'Authorization' : self.token}
        ts = get_timestamp()
        j = {
           'rid': registration[0],
            'reg_type': registration[1],
            'workflowInstanceId': registration[2],
           'isValid': True,
           'internalError': False,
           'messageBusAddress': None,
           'retryCount': None,
            'iteration': 1
        }
        r = requests.post(url, cookies=cookies, json = j, verify=self.ssl_verify)
        r = response_to_json(r)
        return r
