import logging
import time
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class ShareWorks:
    """A class for scraping data from the Shareworks website"""

    def __init__(self, host: str, username: str, passwd: str):
        """Initialize the instance variables for the class methods"""
        self.host = host
        self.username = username
        self.passwd = passwd

    def scrape_data(self, driver) -> dict[str, Any]:
        """Scrape transaction and portfolio data from the Shareworks website"""
        try:
            # Set up wait and log in to Shareworks
            wait = WebDriverWait(driver, 60)
            self.__login(driver, wait)

            # Grab transaction data
            transaction_data = self.__get_transaction_data(driver, wait)

            # Naviagate to portfolio page and change dropdown to GBP
            self.__prepare_portfolio_page(driver, wait)

            # Grab exchange rate, current value, and total shares
            exchange_rate = self.__get_exchange_rate(wait)
            current_value = self.__get_current_value(wait)
            total_shares = self.__get_total_shares(wait)

            # Return the data as a dictionary
            return {
                "transactionData": transaction_data,
                "exchangeRate": exchange_rate,
                "currentValue": current_value,
                "totalShares": total_shares,
            }
        except Exception as exception:
            logging.error(exception)
            return {
                "transactionData": 0,
                "exchangeRate": 0,
                "currentValue": 0,
                "totalShares": 0,
            }
        finally:
            # Ensure the driver is back to default content before exiting
            driver.switch_to.default_content()

    def __login(self, driver: webdriver, wait: WebDriverWait):
        """Log into the website on the driver"""
        # Navigate to the login page
        driver.get("https://" + self.host + "/solium/servlet/userLogin.do")

        # Enter the email and password
        wait.until(
            EC.element_to_be_clickable((By.ID, "account_number_input"))
        ).send_keys(self.username)

        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(
            self.passwd
        )

        # Submit the form
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="submit-box"]/input',
                )
            )
        ).click()

        # Wait until login process has finished and front page has loaded
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="hero-total-portfolio-value"]/span/span[2]')
            )
        )

    def __get_transaction_data(self, driver: webdriver, wait: WebDriverWait) -> list:
        """Open the transaction page, select all history from dropdown
        and collect all transaction history"""
        # Select the Activity Page
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="main-navigation-item-activity"]/a/div/div[2]',
                )
            )
        ).click()

        # Select the reports page
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="App_sticky_sub_nav"]/ul/li[2]/a')
            )
        ).click()

        # Switch the driver to the iframe and wait until the submit button loads
        iframe = driver.find_element(
            By.XPATH, '//*[@id="transaction-statement-iframe"]'
        )
        driver.switch_to.frame(iframe)
        time.sleep(2)
        submit = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submit_html"]'))
        )

        # Select the dropdown and change value to All Available History
        Select(
            driver.find_element(By.XPATH, '//*[@id="date_select"]')
        ).select_by_visible_text("All Available History")

        # Submit the form
        submit.click()

        # Grab all of the rows in the activity table
        rows = driver.find_elements(By.XPATH, '//*[@id="Activity_table"]/tbody/tr')
        transaction_data = []

        # Iterate over the rows
        for row in rows[3:]:
            # Find all the cells in the row
            cells = row.find_elements(By.XPATH, ".//td")

            # Initialize a list to store the data for this row
            row_data = []

            # Iterate over the cells
            for cell in cells:
                # Extract the text from the cell and append it to the row data
                row_data.append(cell.text)

            # Append the row data to the 2D array
            transaction_data.append(row_data)

        # Switch back out of the iframe
        driver.switch_to.default_content()

        # Return the transaction data
        return transaction_data

    def __prepare_portfolio_page(self, driver: webdriver, wait: WebDriverWait):
        """Loads the portfolio page and selects the GBP exchange rate conversion"""
        # Navigate to the portfolio page
        driver.get("https://" + self.host + "/solium/servlet/ui/portfolio/holdings")

        # Select and switch to the iframe
        iframe = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="portfolio-holdings-iframe"]')
            )
        )
        driver.switch_to.frame(iframe)

        # Select British Pound Sterling from conversion dropdown
        Select(
            wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="display_currency"]'))
            )
        ).select_by_visible_text("British Pounds Sterling")

    def __get_exchange_rate(self, wait: WebDriverWait) -> str:
        """Return the current exchange rate shown on the portfolio page"""
        return wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="exchangeRateTable"]/tbody/tr[2]/td[3]')
            )
        ).text.split(" ")[0]

    def __get_current_value(self, wait: WebDriverWait) -> str:
        """Return the current value of all the shares from the Portfolio page"""
        return wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="Transaction View of International Purchase Plan_table"]'
                    + "/tbody/tr[5]/td[3]",
                )
            )
        ).text

    def __get_total_shares(self, wait: WebDriverWait) -> str:
        """Return the total shares from the Portfolio Page"""
        return wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="Transaction View of International Purchase Plan_table"]'
                    + "/tbody/tr[4]/td[4]",
                )
            )
        ).text
