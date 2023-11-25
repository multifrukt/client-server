import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

RETRY_INTERVAL = 5  # Seconds to wait between retries

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def submit_form(url):
    while True:
        try:
            session = requests.Session()
            response = session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            payload = {
                'name': 'Alice',
                'profession': 'Doctor'
            }

            form = soup.find('form', {'id': 'form1'})
            submit_url = url + form['action']
            print(f"[{get_current_time()}] Clicking form at URL: " + submit_url)

            response = session.post(submit_url, data=payload)

            if "API Response" in response.text:
                print(f"[{get_current_time()}] API Response received:" + response.text)
            else:
                print(f"[{get_current_time()}] API Response not found")

            session.close()
            break

        except requests.exceptions.RequestException as e:
            print(f"[{get_current_time()}] Connection to web-front at {url} failed: {e}. Retrying in {RETRY_INTERVAL} seconds...")
            time.sleep(RETRY_INTERVAL)

def main():
    env_var = 'URL_TO_CLICK'
    url = os.environ.get(env_var)
    print(f"Got URL from {env_var} env variable: {url}")

    while True:
        submit_form(url)
        time.sleep(1)

if __name__ == '__main__':
    main()
