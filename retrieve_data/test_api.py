import requests

userid = 1 #your personal user id

def get_user_name(user_id):
    # Define the API endpoint URL
    url = F'https://api.github.com/user/{user_id}'

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except:
        return 'error: filed'

print(get_user_name(userid))