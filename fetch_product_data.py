import requests
import json
from monitor import *
import subprocess
import os
import time
import psutil

MONITOR_PROCESS_NAME = 'monitor.py'
MONITOR_PROCESS_NAME_FETCH = 'fetch_product_data.py'

#to get access token
def get_access_token():
    client_id = 'firstproject-3fcc2e45949f2241762bdf5a99354a304554060350694891851'
    client_secret = 'JdVnuY7H9-MNthNJCM0FLXlPIh277RJbhVOPoggk'
    auth_url = 'https://api.kroger.com/v1/connect/oauth2/token'

    response = requests.post(auth_url, data = {

        'grant_type' : 'client_credentials',
        'client_id' : client_id,
        'client_secret' : client_secret,
        'scope': 'product.compact'
    })


    if response.status_code == 200:
        auth_data = response.json()
        return auth_data['access_token']
        
    else:
        print("Failed to get access token:", response.status_code, response.text)



#to get data.json 
def fetch_product_data():
    print('Collecting product data')
    access_token = get_access_token()
    headers = {
        'Authorization' : f'Bearer {access_token}'
    }

    base_url = 'https://api.kroger.com/v1/products'
    params = {

        'filter.term' : 'milk',
        'filter.limit' : 3
    }

    response = requests.get(base_url, headers = headers, params=params)

    if response.status_code == 200:
        data = response.json()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(script_dir, 'data.json')
        print(data_file_path)
        with open(data_file_path, 'w') as file:
            json.dump(data, file, indent = 4)
        print('------------------------Data saved successfully---------------------------------')
        print(file)
    else:
        print('Failed to fetch data:', response.status_code)
        fetch_product_data()

#to run monitor as a seperate process parallelly
def run_subprocess():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    monitor_script = os.path.join(script_dir,'monitor.py')
    print("inside run_subprocess()")

    if os.path.exists(monitor_script):
        subprocess.Popen(['python', 'monitor.py'])
    else:
        print(f"Error: {monitor_script} does not exist")    

def main():
    # starts monitor
    run_subprocess()

    time.sleep(5)
    #fetch data from kroger
    fetch_product_data()

def kill_monitor_process():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.name().lower() and  MONITOR_PROCESS_NAME in ' '.join(proc.cmdline()).lower():
                proc.terminate()
                print(f'Terminating {MONITOR_PROCESS_NAME} (PID: {proc.pid})')
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    
if __name__ == "__main__":

    if kill_monitor_process():
        print(f'{MONITOR_PROCESS_NAME} process termintaed.')
    else:
        print(f"No {MONITOR_PROCESS_NAME} process found running.")


    print("Current working directory:", os.getcwd())
    main()