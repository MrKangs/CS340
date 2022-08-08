import time
from selenium import webdriver

def refresh_page():
    driver = webdriver.Chrome()
    driver.get(driver.current_url)
    # time.sleep(1)
    driver.refresh()
    # driver.close()