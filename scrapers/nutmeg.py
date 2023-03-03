import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Nutmeg:
    """A class for scraping data from the Nutmeg website"""

    def __init__(self, email, passwd):
        """Initialize the instance variables for the class methods"""
        self.email = email
        self.passwd = passwd

    def scrape_data(self, driver):
        """Scrape transaction and portfolio data from the Nutmeg website"""
        try:
            # Navigate to the login page
            driver.get("https://authentication.nutmeg.com/login/")

            # Wait until the page is loaded and the "Accept Cookies" button is clickable
            wait = WebDriverWait(driver, 20)
            accept_cookies = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_cookies.click()

            # Enter the email and password
            email = wait.until(EC.element_to_be_clickable((By.ID, "username")))
            email.send_keys(self.email)

            password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
            password.send_keys(self.passwd)

            # screenshot = driver.get_screenshot_as_png()
            # with open("screenshot.png", "wb") as f:
            #     f.write(screenshot)

            # Submit the form
            submit = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[3]/div/main/section/div/div/div/form/div[2]/button",
                    )
                )
            )
            submit.click()

            time.sleep(5)

            # Navigae to the transaction history page
            driver.get("https://dashboard.nutmeg.com/transaction-history/general")

            # Get the transaction date
            transaction_date = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table[2]/tbody/tr[1]/td[1]")
                )
            )
            transaction_date = transaction_date.text

            # Navigate to the portfolio page
            driver.get("https://app.nutmeg.com/client/portfolio/dig_deeper")

            # Get the net contributions and the current value
            net_contributions = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table/tbody/tr[1]/th[@class='text-right']")
                )
            )
            net_contributions = net_contributions.text

            current_value = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//table/tbody/tr[4]/th[@class='text-right']")
                )
            )
            current_value = current_value.text

            # Return the data as a dictionary
            return {
                "transactionDate": transaction_date,
                "netContributions": net_contributions,
                "currentValue": current_value,
            }
        except Exception as exception:
            logging.error(exception)
            return {
                "transactionDate": 0,
                "netContributions": 0,
                "currentValue": 0,
            }
