import requests

def call_api(url):
    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            print('Error:', response.status_code)
            return None
    except:
        return f'error: failed calling api for {url}'

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

