# runningohio

Python web service that adds protection on your main branches, for newly created GitHub repos, using GitHub webhooks.

## Prerequisites

Python 3.8+, pip, virtualenv

## Configuration

By default, the app will run on port 5000 and in debug mode. You can update the port and disable debugging on this line.

    app.run(debug=True, port=5000)

This app uses a personal access token for API access. You will also need to update .env to set the environmental variable [GITHUB_SECRET] for GitHub access. This should be a personal access token with the correct repo permissions. To see how to create a personal access token, please go [HERE](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

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

Create .env and add your token

    # cp .env-template .env

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

Enable a Webhook for your organization.

1. Navigate to your organizations account settings.
2. Click on Webhooks in the navbar.
3. Click Add Webhook.
4. Add Payload URL to your web service and select 'application/json' as the content type.
    
![](https://github.com/mikewoodruff/runningohio/blob/feature-branch/docs/webhook1.png?raw=true)

5. Select 'Let me select individual events' under event triggers.
6. Select Repositories.
7. Click Add Webhook

![](https://github.com/mikewoodruff/runningohio/blob/feature-branch/docs/webhook2.png?raw=true)
