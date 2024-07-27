import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Constants for SwagLabs
SWAGLABS_URL = "https://www.saucedemo.com/v1"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

@pytest.fixture(scope="module")
def driver():
    """Fixture for initializing and quitting the WebDriver."""
    driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login(driver):
    driver.get(SWAGLABS_URL)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))

    username_input = driver.find_element(By.ID, "user-name")
    username_input.send_keys(USERNAME)
    time.sleep(0.5)  # Half-second delay

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(PASSWORD)
    time.sleep(0.5)  # Half-second delay

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    time.sleep(0.5)  # Half-second delay

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
    assert "inventory.html" in driver.current_url, "Login failed!"
def test_each_item_add_remove_add_checkout_v1(driver):
    driver.get(SWAGLABS_URL)
    
    test_login(driver)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
    inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    total_items = len(inventory_items)

    for index in range(total_items):
        inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        current_item = inventory_items[index]
        item_title = current_item.find_element(By.CLASS_NAME, "inventory_item_name").text
        print(f"Testing item: {item_title}")

        add_to_cart_button = current_item.find_element(By.CLASS_NAME, "btn_inventory")
        add_to_cart_button.click()

        cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 1, f"Expected 1 item in cart, found {len(cart_items)}."

        remove_button = driver.find_element(By.CLASS_NAME, "cart_button")
        remove_button.click()

        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cart_item")))
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0, "Cart is not empty after removal!"

        driver.find_element(By.CLASS_NAME, "btn_secondary").click()

        inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        current_item = inventory_items[index]

        add_to_cart_button = current_item.find_element(By.CLASS_NAME, "btn_inventory")
        add_to_cart_button.click()

        cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 1, f"Expected 1 item in cart, found {len(cart_items)}."

        checkout_button = driver.find_element(By.CLASS_NAME, "checkout_button")
        checkout_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_info")))

        first_name_input = driver.find_element(By.ID, "first-name")
        first_name_input.send_keys("John")
        last_name_input = driver.find_element(By.ID, "last-name")
        last_name_input.send_keys("Doe")
        postal_code_input = driver.find_element(By.ID, "postal-code")
        postal_code_input.send_keys("12345")

        continue_button = driver.find_element(By.CLASS_NAME, "cart_button")
        continue_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "summary_info")))

        finish_button = driver.find_element(By.CLASS_NAME, "cart_button")
        finish_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))

        confirmation_message = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert confirmation_message == "THANK YOU FOR YOUR ORDER", f"Checkout failed for item: {item_title}"

        # return_home = driver.find_element(By.CLASS_NAME, "btn_secondary")
        # return_home.click()
        driver.get("https://www.saucedemo.com/v1/inventory.html")
        if index == total_items - 1:
            break

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    print("All items have been tested successfully.")


def test_filter_items(driver):
    driver.get(SWAGLABS_URL)
    
    test_login(driver)
    
    def get_item_names():
        items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [item.text for item in items]
    
    filters = {
        "az": "Name (A to Z)",
        "za": "Name (Z to A)",
        "lohi": "Price (low to high)",
        "hilo": "Price (high to low)"
    }
    
    for filter_value, filter_name in filters.items():
        filter_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
        filter_dropdown.click()
        time.sleep(0.5)  # Half-second delay
        
        filter_option = driver.find_element(By.XPATH, f'//option[@value="{filter_value}"]')
        filter_option.click()
        time.sleep(0.5)  # Half-second delay
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name")))
        
        sorted_item_names = get_item_names()
        
        if filter_value == "az":
            assert sorted_item_names == sorted(sorted_item_names), "Items are not sorted A to Z"
        elif filter_value == "za":
            assert sorted_item_names == sorted(sorted_item_names, reverse=True), "Items are not sorted Z to A"
        elif filter_value == "lohi":
            prices = [float(item.find_element(By.CLASS_NAME, "inventory_item_price").text[1:]) for item in driver.find_elements(By.CLASS_NAME, "inventory_item")]
            assert sorted_item_names == [x for _, x in sorted(zip(prices, sorted_item_names))], "Items are not sorted low to high"
        elif filter_value == "hilo":
            prices = [float(item.find_element(By.CLASS_NAME, "inventory_item_price").text[1:]) for item in driver.find_elements(By.CLASS_NAME, "inventory_item")]
            assert sorted_item_names == [x for _, x in sorted(zip(prices, sorted_item_names), reverse=True)], "Items are not sorted high to low"
        
        print(f"Filter '{filter_name}' applied and verified.")
        time.sleep(1)  
    print("All filters tested successfully.")
     
def test_logout_app(driver):
    menu_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "bm-burger-button")))
    menu_button.click()
    time.sleep(0.5)  

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "inventory_sidebar_link")))

    logout_button = driver.find_element(By.ID, "logout_sidebar_link")
    logout_button.click()
    time.sleep(0.5)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
    assert "inventory.html" not in driver.current_url, "Logout failed!"

    print("Test Passed: Logout successful.")
