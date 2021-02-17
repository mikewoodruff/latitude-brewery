#!/usr/bin/env python3

# imports
import os
import requests
import json
import time
from flask import Flask, make_response, request

# functions
def set_branch_protection(org, repo, branch):
    try:
        # add headers for token and api version
        headers = {
            'Authorization': 'token ' + os.getenv('GITHUB_SECRET'),
            'Accept': 'application/vnd.github.v3+json'
        }
        # build uir
        uri = 'https://api.github.com/repos/{}/{}/branches/{}/protection'.format(org, repo, branch)
        # build body
        body = {
            'required_status_checks' : {
                'include_admins' : False,
                'strict' : True,
                'contexts' : ['default']
            },
            'required_pull_request_reviews' : {
                'include_admins' : False
            },
            'restrictions' : None,
            'enforce_admins' : False
        }
        json_body = json.dumps(body)
        # send PUT request
        request = requests.put(uri, data=json_body, headers=headers, verify=False)
        return request
    except Exception as e:
        print(e)

def get_branch_protection(org, repo, branch):
    try:
        # add headers for token and api version
        headers = {
            'Authorization': 'token ' + os.getenv('GITHUB_SECRET'),
            'Accept': 'application/vnd.github.v3+json'
        }
        # build uir
        uri = 'https://api.github.com/repos/{}/{}/branches/{}'.format(org, repo, branch)
        # send GET request
        request = json.loads(requests.get(uri, headers=headers, verify=False).content)
        if request['protected'] == True:
            return True
        else:
            return False
    except Exception as e:
        print(e)

# create app instance
app = Flask(__name__)

# default route
@app.route('/')
def hello_world():
    return 'Welcome!'

# api route for protecting branch
@app.route('/api/v1/branches/protect', methods=['PATCH'])
def main():
    try:
        # get branch id from form
        branch = request.form.get('branch')
        org = request.form.get('org')
        repo = request.form.get('repo')
        # protect branch if all required params
        if len(branch) > 0 and len(org) > 0 and len(repo) > 0:
            # enabled protection
            set_protection = set_branch_protection(org, repo, branch)
            # sleep for a few seconds to allow the next call to return successfully
            time.sleep(3)
            # test to see if protection exists
            get_protection = get_branch_protection(org, repo, branch)
            if get_protection == True:
                # return successful  response
                return make_response(
                    json.dumps({'Success':True}),
                    200
                )
            else:
                # something went wrong
                # return response
                return make_response(
                    json.dumps({'Error':'Something went wrong there!'}),
                    400
                )
        else:
            # do not have all parameters needed
            # return response
            return make_response(
                json.dumps({'Error':'Please specify the correct parameters (branch, owner, repo)'}),
                400
            )
    except Exception as e:
        # return exception
        return make_response(
            json.dumps({'Error':e}),
            500
        )

# start app
app.run(debug=True, port=5000)