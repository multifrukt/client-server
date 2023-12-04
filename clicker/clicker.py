import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

ENV_VAR_URL_TO_CLICK = 'URL_TO_CLICK'
ENV_VAR_RETRY_ON_SUCCESS_INTERVAL = 'RETRY_ON_SUCCESS_INTERVAL'
ENV_VAR_RETRY_ON_FAILURE_INTERVAL = 'RETRY_ON_FAILURE_INTERVAL'


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    url_to_click = os.environ.get(ENV_VAR_URL_TO_CLICK)
    print(f"Got Environment variable {ENV_VAR_URL_TO_CLICK}: {url_to_click}")

    retry_on_success_interval = float(
        os.environ.get(ENV_VAR_RETRY_ON_SUCCESS_INTERVAL))  # Seconds
    print(f"Got Environment variable {ENV_VAR_RETRY_ON_SUCCESS_INTERVAL}: {retry_on_success_interval}")

    retry_on_failure_interval = float(
        os.environ.get(ENV_VAR_RETRY_ON_FAILURE_INTERVAL))  # Seconds
    print(f"Got Environment variable {ENV_VAR_RETRY_ON_FAILURE_INTERVAL}: {retry_on_failure_interval}")

    while True:
        try:
            session = requests.Session()
            response = session.get(url_to_click)
            soup = BeautifulSoup(response.text, 'html.parser')

            payload = {
                'name': 'Alice',
                'profession': 'Doctor'
            }

            form = soup.find('form', {'id': 'form1'})
            submit_url = url_to_click + form['action']
            print(f"[{get_current_time()}] Clicking form at URL: " + submit_url)

            response = session.post(submit_url, data=payload)

            if "API Response" in response.text:
                print(f"[{get_current_time()}] API Response received:" + response.text)
            else:
                print(f"[{get_current_time()}] API Response not found")

            session.close()

            print(
                f"[{get_current_time()}] Connection to web-front at {url_to_click} succeeded."
                f" Retrying in {retry_on_success_interval} seconds...")
            time.sleep(retry_on_success_interval)

        except requests.exceptions.RequestException as e:
            print(
                f"[{get_current_time()}] Connection to web-front at {url_to_click} failed: {e}."
                f" Retrying in {retry_on_failure_interval} seconds...")
            time.sleep(retry_on_failure_interval)


if __name__ == '__main__':
    main()
