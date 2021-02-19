# runningohio

Python web service that adds protection on your main branches, for newly created GitHub repos, using GitHub webhooks.

## Prerequisites

Python 3.8+, pip, virtualenv

## Configuration

By default, the app will run on port 5000 and in debug mode. You can update the port and disable debugging on this line.

    app.run(debug=True, port=5000)

You will also need to update .env to set the environmental variable [GITHUB_SECRET] for GitHub access. This should be an access token with the correct repo permissions.

    GITHUB_SECRET=TOKEN

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

    # curl -d '{"repository": {"default_branch": "main", "name": "test-repo"}, "organization": {"login": "running-ohio"}}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/branches/protect

### Python

    # import requests
    # import json
    headers = {
        'Accept': 'application/json'
    }
    # data = {
        'repository':{
            'default_branch': 'main',
            'name': 'test-repo'
        },
        'organization':{
            'login': 'running-ohio'
        }
    }
    # requests.post('http://127.0.0.1:5000/api/v1/branches/protect', json = data, headers = headers)

## Enable Webhook

Enable webhook for your organization.
    1. Navigate to your organizations account settings.
    2. Click on Webhooks in the navbar.
    3. Click Add Webhook.
    
![Add Webhook](https://github.com/mikewoodruff/runningohio/tree/feature-branch/docs/webhook1.png)
![Select Repo](https://github.com/mikewoodruff/runningohio/tree/feature-branch/docs/webhook2.png)
