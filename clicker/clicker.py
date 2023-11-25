import os
import time
import requests
from bs4 import BeautifulSoup

# Replace 'field1_name', 'field2_name' with the actual names of the HTML fields
def submit_form(url):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming the fields are input fields, you might need to adjust this for different HTML structures
    payload = {
        'name': 'Alice',
        'profession': 'Doctor'
    }

    # Replace 'form_id_or_name' with the actual ID or name of the form
    form = soup.find('form', {'id': 'form1'})
    submit_url = url + form['action']
    print("Clicking form at URL: " + submit_url)

    response = session.post(submit_url, data=payload)

    if "API Response" in response.text:
        print("API Response received:" + response.text)
    else:
        print("API Response not found")

    session.close()

def main():
    env_var = 'URL_TO_CLICK'
    url = os.environ.get(env_var)
    print("Got URL from " + env_var + " env variable: " + url)

    while True:
        submit_form(url)
        time.sleep(1)

if __name__ == '__main__':
    main()
