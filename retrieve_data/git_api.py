import requests
from dotenv import load_dotenv
import os
import time

load_dotenv('../.env')

def call_api(url):
    result = []
    url = url + '?per_page=100'
    res = exec_api(url)
    result += res.json()
    next = [link[1:-13] for link in res.headers['Link'].split(',') if link.find('rel="next"') > 0]
    while len(next) == 1:
        print('getting next page' + next[0])
        res = exec_api(next[0])
        result += res.json()
        next = [link[1:-13] for link in res.headers['Link'].split(',') if link.find('rel="next"') > 0]
    return result

gittoken = os.getenv('GITHUB_TOKEN')
timeout = 720

def exec_api(url):
    epoch = int(time.time())
    try:
        # Make a GET request to the API endpoint using requests.get()
        headers = {'content-type': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'Authorization': 'Bearer ' + gittoken}
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            res = response
            return res
        else:
            print('Error:', response.status_code)
            return None
    except:
        return f'error: failed calling api for {url}'
    newepoch = int(time.time())
    if(epoch + timeout > newepoch):
        sleep((epoch+timeout) - newepoch)

def get_user(user_id):
    # Define the API endpoint URL
    url = F'https://api.github.com/user/{user_id}'
    res = call_api(url)
    return res

def get_project_owner_and_name(issue_tread_url):
    return issue_tread_url[29:].split('/')[0], issue_tread_url[29:].split('/')[1]


def get_repository_activity(owner, repo):
    url = F'https://api.github.com/repos/{owner}/{repo}/activity'
    res = call_api(url)
    return res

def get_repository_commits(owner, repo):
    url = F'https://api.github.com/repos/{owner}/{repo}/commits'
    res = call_api(url)
    return res

def parse_repository_activity(res):
    result = []

