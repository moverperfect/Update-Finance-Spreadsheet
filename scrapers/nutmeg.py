# pylint: disable=R0903
# pylint: disable=W0718
"""Module providing logging"""
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Nutmeg:
    """A class for scraping data from the Nutmeg website"""

    def __init__(self, driver, email, passwd):
        """Initialize the instance variables for the class methods"""
        self.driver = driver
        self.email = email
        self.passwd = passwd

    def scrape_data(self):
        """Scrape transaction and portfolio data from the Nutmeg website"""
        try:
            # Use the driver instance
            with self.driver as driver:
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

                password = driver.find_element_by_id("password")
                password.send_keys(self.passwd)

                # screenshot = driver.get_screenshot_as_png()
                # with open("screenshot.png", "wb") as f:
                #     f.write(screenshot)

                # Submit the form
                submit = driver.find_element_by_xpath(
                    "//form/div[@class='c90e953d1']/button"
                )
                submit.click()

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