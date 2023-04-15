from datetime import datetime
import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Nutmeg:
    """A class for scraping data from the Nutmeg website"""

    def __init__(self, email, passwd):
        """Initialize the instance variables for the class methods"""
        self.email = email
        self.passwd = passwd

    def scrape_data(self, driver: WebDriver):
        """Scrape transaction and portfolio data from the Nutmeg website"""
        try:
            wait = WebDriverWait(driver, 20)

            output = {}

            # Log into the website
            self.__login(driver, wait)

            # Grab Transaction History
            output["transactions"] = self.__get_transaction_data(driver, wait)

            # Grab portfolio data
            output.update(self.__get_portfolio_data(driver, wait))

            # Return the data as a dictionary
            return output

        except Exception as exception:
            logging.error(exception)
            return {
                "transactions": [],
                "netContributions": 0,
                "currentValue": 0,
            }

    def __login(self, driver: WebDriver, wait: WebDriverWait):
        """
        Log in to the Nutmeg authentication page using the provided email and password.

        :param driver: The WebDriver instance used for browser automation.
        :param wait: The WebDriverWait instance for waiting on elements to load.
        """
        # Navigate to the login page
        driver.get("https://authentication.nutmeg.com/login/")

        # Wait until the page is loaded and the "Accept Cookies" button is clickable
        accept_cookies = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies.click()

        # Wait for the email input field to be visible and enter the email
        email_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        email_field.send_keys(self.email)

        # Wait for the password input field to be visible and enter the password
        password_field = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_field.send_keys(self.passwd)

        # Wait for the submit button to be clickable and click it
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit.click()

        time.sleep(5)

    def __get_transaction_data(self, driver: WebDriver, wait: WebDriverWait):
        """
        Retrieve transaction data from the Nutmeg dashboard transaction history page.

        :param driver: WebDriver instance for web scraping.
        :param wait: WebDriverWait instance for waiting for elements to load.
        :return: List of dictionaries containing transaction data.
        """
        # Navigate to the transaction history page
        driver.get("https://dashboard.nutmeg.com/transaction-history/general")

        # Wait for the table to load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

        # Initialize list to store transaction data
        transactions_data = []

        # Find all table elements and header elements on the page
        tables = driver.find_elements(By.CSS_SELECTOR, "table")
        headers = driver.find_elements(
            By.XPATH,
            '//*[@id="root"]/section/section[2]/div/div/div/div/section/div/section[2]'
            + "/section/section/h1/span",
        )

        # Iterate over each table and its corresponding header
        for index, table in enumerate(tables):
            # Find all transaction rows within the table
            transactions = table.find_elements(By.CSS_SELECTOR, "tbody tr")

            # Parse and format the month from the header text
            month_parts = headers[index].text.split()
            month_parts[0] = month_parts[0][:3]
            month = datetime.strptime(" ".join(month_parts), "%b %Y")

            # Iterate over each transaction row
            for transaction in transactions:
                transaction_data = {}
                transaction_cells = transaction.find_elements(By.CSS_SELECTOR, "td")

                # Extract and format the day, transaction type, pot, and amount from
                # the transaction cells
                day = int(transaction_cells[0].text.split()[1])
                transaction_data["date"] = datetime(month.year, month.month, day)
                transaction_data["transaction"] = transaction_cells[1].text
                transaction_data["pot"] = transaction_cells[2].text

                # Filter out unwanted transaction data
                if (
                    transaction_data["pot"] == "Unallocated Cash"
                ):
                    continue

                # Remove unnecessary characters from the amount string and add the
                # amount to the transaction data
                transaction_data["amount"] = (
                    transaction_cells[3].text.replace("+", "").replace("£", "")
                )
                transactions_data.append(transaction_data)

        return transactions_data

    def __get_portfolio_data(self, driver: WebDriver, wait: WebDriverWait):
        """
        Get the portfolio data from the Nutmeg website.

        :param driver: A WebDriver instance for browser automation.
        :param wait: A WebDriverWait instance for waiting for elements to load.
        :return: A dictionary containing the net contributions
        and current value of the portfolio.
        """

        # Navigate to the portfolio page
        driver.get("https://app.nutmeg.com/client/portfolio/dig_deeper")

        # Define the XPaths for net contributions and current value
        net_contributions_xpath = "//table/tbody/tr[1]/th[@class='text-right']"
        current_value_xpath = "//table/tbody/tr[4]/th[@class='text-right']"

        # Wait for the net contributions element to be present, then get its text
        net_contributions = wait.until(
            EC.presence_of_element_located((By.XPATH, net_contributions_xpath))
        ).text

        # Wait for the current value element to be present, then get its text
        current_value = wait.until(
            EC.presence_of_element_located((By.XPATH, current_value_xpath))
        ).text

        # Return the portfolio data as a dictionary
        return {
            "netContributions": net_contributions,
            "currentValue": current_value,
        }
