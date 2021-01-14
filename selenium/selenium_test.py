from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import datetime

# Ititialize settings
login_url = 'https://www.saucedemo.com/'
LOG_FILE = "/var/logs/selenium/selenium_log.txt"
log_arr = []


# def create_driver():
#     log('Starting the browser...')
#     options = ChromeOptions()
#     options.add_argument("--headless") 
#     return webdriver.Chrome(options=options)

def log(text):
    time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SK")
    entry = time + " " + text
    print(entry)
    log_arr.append(entry)


def write_log():
    with open(LOG_FILE, "a+") as txt_file:
        for line in log_arr:
            txt_file.write("".join(line) + "\n")


# def login(driver, user, password):
def login(user, password):
    log('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    log('Test: login. Navigating to the demo page to login {}'.format(login_url))
    driver.get(login_url)
    log('Login attempt, user: {},  password: {}'.format(user, password))
    driver.find_element_by_id('user-name').send_keys(user)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('login-button').click()
    assert inventory_url in driver.current_url
    log('Login Successful.')
    driver.close()
    write_log()

# login(driver, 'standard_user', 'secret_sauce')
login('standard_user', 'secret_sauce')
