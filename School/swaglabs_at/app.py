from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
i
SWAGLABS_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

driver = webdriver.Chrome()  # Make sure chromedriver is in your PATH

try:
    driver.get(SWAGLABS_URL)

    driver.maximize_window()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "user-name")))

    username_input = driver.find_element(By.ID, "user-name")
    time.sleep(1)
    username_input.send_keys(USERNAME)
    password_input = driver.find_element(By.ID, "password")
    time.sleep(1)
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.ID, "login-button")
    time.sleep(1)
    login_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    time.sleep(1)
    add_to_cart_button = driver.find_element(By.XPATH, '//button[contains(@id, "add-to-cart")]')
    time.sleep(1)
    add_to_cart_button.click()

    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    time.sleep(1)
    cart_icon.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    checkout_button = driver.find_element(By.ID, "checkout")
    time.sleep(1)
    checkout_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name")))

    first_name_input = driver.find_element(By.ID, "first-name")
    time.sleep(1)
    first_name_input.send_keys("John")

    last_name_input = driver.find_element(By.ID, "last-name")
    time.sleep(1)
    last_name_input.send_keys("Doe")

    postal_code_input = driver.find_element(By.ID, "postal-code")
    time.sleep(1)
    postal_code_input.send_keys("12345")

    continue_button = driver.find_element(By.ID, "continue")
    time.sleep(1)
    continue_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "summary_info")))

    finish_button = driver.find_element(By.ID, "finish")
    time.sleep(1)
    finish_button.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))

    confirmation_message = driver.find_element(By.CLASS_NAME, "complete-header").text
    time.sleep(1)
    assert confirmation_message == "THANK YOU FOR YOUR ORDER", "Checkout failed!"

    print("Test Passed: Checkout completed successfully.")

except TimeoutException:
    print("Test Failed: Timeout occurred during testing.")
except AssertionError as e:
    print(f"Test Failed: {str(e)}")
finally:
    driver.quit()
