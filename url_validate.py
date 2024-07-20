import validators
import requests
from DBworks import *
from datetime import datetime
import psutil

#url validation 
URL_PROCESS_NAME = 'url_validate.py'


def is_valid_url(url):
    return validators.url(url)

def is_url_reachable(url, headers):
    try:
        params = {'filter.term': 'milk', 'filter.limit': 1}
        response = requests.get(url, headers=headers, params=params, allow_redirects=True)
        print(f"Response status code: {response.status_code}")
        return response.status_code < 400
    except requests.RequestException as e:
        print(f"RequestException occurred: {e}")
        return False



def validate_url(url, headers):
    #validate url format and reachability
    if is_valid_url(url):
        print(f'URL format is valid: {url}')
        column_format = "URL is valid"
        if is_url_reachable(url, headers):
            column_reach = "URL is reachable"
            print(f"URL is reachable: {url}")
            return True, column_format, column_reach
        else:
            column_reach = "URL is not reachable"
            print(f"URL is not reachable: {url}")
            return False, column_format, column_reach
    else:
        print(f"URL format is not valid: {url}")
        column_format = "URL is not valid"
        column_reach = "So ,URL is not reachable"
        return False, column_format, column_reach


def run():
    #Kroger API url 
    base_url = 'https://api.kroger.com/v1/products'
    client_id = 'firstproject-3fcc2e45949f2241762bdf5a99354a304554060350694891851'
    client_secret = 'JdVnuY7H9-MNthNJCM0FLXlPIh277RJbhVOPoggk'
    auth_url = 'https://api.kroger.com/v1/connect/oauth2/token'

    #Token access
    response = requests.post(auth_url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'product.compact'
    })

    if response.status_code == 200:
        auth_data = response.json()
        access_token = auth_data['access_token']
        headers = {'Authorization' : f'Bearer {access_token}'}
        
        val_url = validate_url(base_url, headers)
        #validate kroger api
        if val_url[0]:
            valid = val_url[1]
            reach = val_url[2]
            times = datetime.now()
            time_str = times.strftime("%Y-%m-%d %I:%M:%S %p")
            val = (valid, reach, time_str)
            query = "insert into validation_info values(%s, %s, %s)"
            iud(query,val)
            print('Kroger API url is valid and reachable')
        else:
            print("Kroger API url is not reachable.")
    else:
        print('Failed to get access token:', response.status_code, response.text)



def kill_url_process():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.name().lower() and URL_PROCESS_NAME in ' '.join(proc.cmdline()).lower():
                proc.terminate
                print(f"Terminating {URL_PROCESS_NAME} (PID: {proc.pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass



if __name__ == '__main__':
    if kill_url_process():
        print(f"{URL_PROCESS_NAME} process terminated")
    else:
        print(f"No {URL_PROCESS_NAME} is running")

    run()