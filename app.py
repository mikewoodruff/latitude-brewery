#!/usr/bin/env python3

# imports
import os
import requests
import json
import time
from flask import Flask, make_response, request

## functions
# enable protection on branch
def enable_branch_protection(org, repo, branch):
    try:
        # add headers for token and api version
        headers = {
            'Authorization': 'token ' + os.getenv('GITHUB_SECRET'),
            'Accept': 'application/vnd.github.+json',
            'Accept': 'application/json'
        }
        # build uri
        uri = '{}/repos/{}/{}/branches/{}/protection'.format(os.getenv('GITHUB_URI'), org, repo, branch)
        # build body
        body = {
            'required_status_checks': {
                'enforce_admins': True,
                'strict': True,
                'contexts': ['default']
            },
            'required_pull_request_reviews': {
                'require_code_owner_reviews': True
            },
            'restrictions': None,
            'enforce_admins' : True
        }
        json_body = json.dumps(body)
        # send PUT request
        request = requests.put(uri, data=json_body, headers=headers, verify=False)
        if request.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)

# get branch protection
def get_branch_protection(org, repo, branch):
    try:
        # add headers for token and api version
        headers = {
            'Authorization': 'token ' + os.getenv('GITHUB_SECRET'),
            'Accept': 'application/vnd.github.v3+json'
        }
        # build uri
        uri = '{}/repos/{}/{}/branches/{}'.format(os.getenv('GITHUB_URI'), org, repo, branch)
        # send GET request
        request = json.loads(requests.get(uri, headers=headers, verify=False).content)
        if request['protected']:
            return True
        else:
            return False
    except Exception as e:
        print(e)

# create new issue with @mention
def new_issue(org, repo):
    try:
        # add headers for token and api version
        headers = {
            'Authorization': 'token ' + os.getenv('GITHUB_SECRET'),
            'Accept': 'application/vnd.github.v3+json'
        }
        body = {
            'title': 'Main branch protection added',
            'body': '@mikewoodruff heads up! Branch protection was added successfully to main. \n\n' \
                    '**Protection Added** \n' \
                    ' - Require pull request reviews before merging \n' \
                        '   - Required approving reviews: 1 \n' \
                        '   - Require review from Code Owners \n' \
                    ' - Require status checks to pass before merge \n' \
                        '   - Require branches to be up to date before merging \n' \
                        '   - Status checks: default \n' \
                    ' - Include Administrators \n'
        }
        json_body = json.dumps(body)
        # build uri
        uri = '{}/repos/{}/{}/issues'.format(os.getenv('GITHUB_URI'), org, repo)
        # send GET request
        request = requests.post(uri, data=json_body, headers=headers, verify=False)
        if request.status_code == 201:
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
@app.route('/api/v1/branches/protect', methods=['POST'])
def main():
    try:
        # get post data
        content = request.json
        # get branch id from form
        branch = content['repository']['default_branch']
        org = content['organization']['login']
        repo = content['repository']['name']
        # protect branch if all required params
        if branch and org and repo:
            # enabled protection
            enable_protection = enable_branch_protection(org, repo, branch)
            # if protection was set, check repo to verify
            if enable_protection:
                # sleep for a second to allow the next call to return successfully
                time.sleep(1)
                # test to see if protection exists
                get_protection = get_branch_protection(org, repo, branch)
                if get_protection:
                    # create new issue
                    new_issue(org, repo)
                    # return successful response
                    return make_response(
                        json.dumps({'Success':True}),
                        200
                    )
                else:
                    # get_protection=False
                    # return response
                    return make_response(
                        json.dumps({'Error':'Something went wrong there!'}),
                        400
                    )
            else:
                # enable_protection=False
                # return response
                return make_response(
                    json.dumps({'Error':'Something went wrong while enabling protection!'}),
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
if __name__ == '__main__':
    app.run(debug=True, port=5000)