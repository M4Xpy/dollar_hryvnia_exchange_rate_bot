from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_exchange_rate():
    url = 'https://www.google.com/finance/quote/USD-UAH'
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for the title to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'title')))

    title = driver.title

    driver.quit()

    return title.split()[1]


if __name__ == '__main__':
    print(get_exchange_rate())
