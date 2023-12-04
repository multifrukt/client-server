import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

ENV_VAR_URL_TO_CLICK = 'URL_TO_CLICK'
ENV_VAR_RETRY_ON_SUCCESS_INTERVAL = 'RETRY_ON_SUCCESS_INTERVAL'
ENV_VAR_RETRY_ON_FAILURE_INTERVAL = 'RETRY_ON_FAILURE_INTERVAL'


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    url_to_click = os.environ.get(ENV_VAR_URL_TO_CLICK)
    print(f"Got Environment variable {ENV_VAR_URL_TO_CLICK}: {url_to_click}")

    retry_on_success_interval = float(os.environ.get(ENV_VAR_RETRY_ON_SUCCESS_INTERVAL))  # Seconds
    print(f"Got Environment variable {ENV_VAR_RETRY_ON_SUCCESS_INTERVAL}: {retry_on_success_interval}")

    retry_on_failure_interval = float(os.environ.get(ENV_VAR_RETRY_ON_FAILURE_INTERVAL))  # Seconds
    print(f"Got Environment variable {ENV_VAR_RETRY_ON_FAILURE_INTERVAL}: {retry_on_failure_interval}")

    # Initialize counters and timers
    total_count = 0
    last_log_time = time.time()
    tries_statistics = ""

    while True:
        total_count += 1

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
            print(f"[{timestamp()}] Clicking form at URL: " + submit_url)

            response = session.post(submit_url, data=payload)

            if "API Response" in response.text:
                print(f"[{timestamp()}] API Response received:" + response.text)
            else:
                print(f"[{timestamp()}] API Response not found")

            session.close()

            print(f"[{timestamp()}] Connection to web-front at {url_to_click} succeeded."
                  f" Retrying in {retry_on_success_interval} seconds...")
            time.sleep(retry_on_success_interval)

        except requests.exceptions.RequestException as e:
            print(f"[{timestamp()}] Connection to web-front at {url_to_click} failed: {e}."
                  f" Retrying in {retry_on_failure_interval} seconds...")
            time.sleep(retry_on_failure_interval)

        # Calculate statistics
        current_time = time.time()
        if current_time - last_log_time >= 60:
            minutes_elapsed = (current_time - last_log_time) / 60
            tries_per_minute = total_count / minutes_elapsed
            tries_per_second = tries_per_minute / 60
            tries_statistics = (f"Tries per minute: {tries_per_minute:.2f}\n"
                                f"Tries per second: {tries_per_second:.2f}\n"
                                f"Note: Statistics refresh every 1 minute. Last refresh was: [{timestamp()}]")

            # Reset counters and timestamp
            total_count = 0
            last_log_time = current_time

        if tries_statistics:
            print(tries_statistics)
        else:
            print(f"[{timestamp()}] Statistics are being collected and will be available after the first minute elapses.")


if __name__ == '__main__':
    main()
