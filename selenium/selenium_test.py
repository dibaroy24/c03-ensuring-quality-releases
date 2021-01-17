from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import datetime

# Ititialize settings
login_url = 'https://www.saucedemo.com/'
inventory_url = 'https://www.saucedemo.com/inventory.html'
cart_url = 'https://www.saucedemo.com/cart.html'
LOG_FILE = "/var/logs/selenium/selenium_log.txt"
log_arr = []


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
    log('Test: Login. Navigating to the demo page to login {}'.format(login_url))
    driver.get(login_url)
    log('Login attempt, user: {},  password: {}'.format(user, password))
    driver.find_element_by_id('user-name').send_keys(user)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('login-button').click()
    assert inventory_url in driver.current_url
    log('Login Successful.')



    items_in_cart = []
    log('Test: Adding items to cart')
    elements = driver.find_elements_by_class_name('inventory_item')
    for item in elements:
        item_name = item.find_element_by_class_name('inventory_item_name').text
        items_in_cart.append(item_name)
        item.find_element_by_class_name('btn_inventory').click()
        log('Added {} to cart'.format(item_name))
    cart_element = driver.find_element_by_class_name('shopping_cart_badge')
    assert int(cart_element.text) == len(elements)
    #print ('Navigate to cart and assert items in cart.')
    driver.find_element_by_class_name('shopping_cart_link').click()
    assert cart_url in driver.current_url
    for item in driver.find_elements_by_class_name('inventory_item_name'):
        assert item.text in items_in_cart
    log('Successfully Added Items in cart.')


    log('Test: Removing items from cart')
    #print ('Navigate to cart and assert items in cart.')
    driver.find_element_by_class_name('shopping_cart_link').click()
    assert cart_url in driver.current_url

    log("Items in Cart: {}".format(len(driver.find_elements_by_class_name('cart_item'))))
    
    #print('Remove all items from cart.')
    for item in driver.find_elements_by_class_name('cart_item'):
        item_name = item.find_element_by_class_name('inventory_item_name').text
        item.find_element_by_class_name('cart_button').click()
        log('Removed {} from cart'.format(item_name))

    assert len(driver.find_elements_by_class_name('cart_item')) == 0
    #print('Cart empty.')
    log('Successfully Removed Items from the cart.')

    driver.close()
    write_log()

# login(driver, 'standard_user', 'secret_sauce')
login('standard_user', 'secret_sauce')
