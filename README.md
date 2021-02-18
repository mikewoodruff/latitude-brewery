# runningohio

Python web service that adds protection on your main branches, for newly created GitHub repos, using GitHub webhooks.

## Prerequisites

Python 3.8+, pip, virtualenv

## Configuration

By default, the app will run on port 5000 and in debug mode. You can update the port and disable debugging on this line.

    app.run(debug=True, port=5000)

## Installing

First, clone the repository

    # git clone http://github.com/mikewoodruff/runningohio
    # cd runningohio

Create a virtualenv, and activate it

    # virtualenv env 
    # source env/bin/activate

Install requirements

    # pip install -r requirements.txt

Run the app!

    # python3 app.py

## Testing

### curl

    # curl -d '{"org": "running-ohio", "repo": "test-repo", "branch": "main"}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/branches/protect

### Python

    # import requests
    # import json
    headers = {
        'Accept': 'application/json'
    }
    # data = {
        'org':'running-ohio',
        'repo':'test-repo',
        'branch':'main'
    }
    # json = json.dumps(data)
    # requests.post('http://127.0.0.1:5000/api/v1/branches/protect', data = json, headers = headers)

## Enable Webhook

Enable webhook for your organization
