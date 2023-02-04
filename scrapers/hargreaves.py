import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver


class Hargreaves:
    """A class for scraping data from the Hargreaves Lansdown website"""

    def __init__(
        self,
        driver: webdriver,
        username: str,
        dob: str,
        password: str,
        secure_number: str,
        accounts: list,
    ):
        """Initialize the instance variables for the class methods"""
        self.driver = driver
        self.username = username
        self.dob = dob
        self.password = password
        self.secure_number = secure_number
        self.accounts = accounts

    def scrape_data(self) -> list(dict[str, str]):
        """Scrape transaction and portfolio data from the Hargreaves Lansdown website"""
        try:
            # Use the driver instance
            with self.driver as driver:
                # Log into the website
                self.__login(driver)

                accounts_data = []

                # For each defined account, check holdings and transactions
                for account in self.accounts:
                    accounts_data.append(self.__check_account(driver, account))

                # Return the data as a dictionary
                return accounts_data
        except Exception as exception:
            logging.error(exception)
            return []

    def __login(self, driver: webdriver):
        """Log into the website on the driver"""
        # Navigate to the login page
        driver.get("https://online.hl.co.uk/my-accounts/login-step-one")

        # Wait until the page is loaded and enter the username and Date of Birth
        wait = WebDriverWait(driver, 20)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="acceptCookieButton"]'))
        ).click()

        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(
            self.username
        )

        wait.until(EC.element_to_be_clickable((By.ID, "date-of-birth"))).send_keys(
            self.dob
        )

        # Submit the form
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="login"]/div[3]/p[1]/input',
                )
            )
        ).click()

        # Enter the password
        wait.until(
            EC.element_to_be_clickable((By.ID, "online-password-verification"))
        ).send_keys(self.password)

        # Get the secret numbers that need to be inserted
        secure_number_elements = driver.find_elements(
            By.XPATH, '//div[@class="secure-number-container__label"]'
        )

        # Loop through each secure number that need to be inserted
        for x, element in enumerate(secure_number_elements):
            # Check which digit in the secure number needs to be inserted
            label = element.text[:1]
            # Insert the required digit into input
            driver.find_element(
                By.XPATH,
                '//div[@class="secure-number-container__label"]['
                + str(x + 1)
                + "]/div/input",
            ).send_keys(self.secure_number[int(label) - 1])

        # Submit the form
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="submit"]',
                )
            )
        ).click()

        # Wait until user log in is complete
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="breadcrumbs"]/div[1]/strong[1]')
            )
        )

    def __check_account(self, driver: webdriver, account_number: str) -> dict[str, str]:
        """Check the account number and return value, stocks, and transactions"""
        account_data = {"value": 0, "stocks": [], "transactions": []}

        wait = WebDriverWait(driver, 20)

        # Navigate to the account summary page for the account_number
        driver.get(
            "https://online.hl.co.uk/my-accounts/account_summary/account/"
            + str(account_number)
        )

        # Grab the account value
        account_data["value"] = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="account_total_header"]'))
        ).text

        # Grab the stocks in the account
        account_data["stocks"] = self.__get_stock_data(driver)

        # Grab the transactions in the account
        account_data["transactions"] = self.__get_transaction_data(
            driver, wait, account_number
        )

        return account_data

    def __get_stock_data(self, driver: webdriver) -> list:
        """Return the stock data from the account summary page
        Account summary page must be opened prior to function call"""
        stocks_data = []

        # Grab the rows of stocks
        stocks = driver.find_elements(By.XPATH, '//*[@id="holdings-table"]/tbody/tr')

        # For each stock, grab name, units, price, value, and cost
        for x in range(1, len(stocks)):
            stock_data = {}
            stock_data["stock"] = driver.find_element(
                By.XPATH,
                '//*[@id="holdings-table"]/tbody/tr[' + str(x) + "]/td[1]/div/a/span",
            ).text
            stock_data["units"] = driver.find_element(
                By.XPATH,
                '//*[@id="holdings-table"]/tbody/tr[' + str(x) + "]/td[2]/span",
            ).text
            stock_data["price(p)"] = driver.find_element(
                By.XPATH,
                '//*[@id="holdings-table"]/tbody/tr[' + str(x) + "]/td[3]/span",
            ).text
            stock_data["value"] = driver.find_element(
                By.XPATH,
                '//*[@id="holdings-table"]/tbody/tr[' + str(x) + "]/td[4]/span/span",
            ).text
            stock_data["cost"] = driver.find_element(
                By.XPATH,
                '//*[@id="holdings-table"]/tbody/tr[' + str(x) + "]/td[5]/span",
            ).text
            stocks_data.append(stock_data)

        return stocks_data

    def __get_transaction_data(
        self, driver: webdriver, wait: WebDriverWait, account_number: str
    ) -> list:
        """Return the transaction data from the transactions page.
        Function will navigate to page"""

        # Navigate to transaction history page
        driver.get(
            "https://online.hl.co.uk/my-accounts/capital-transaction-history/account/"
            + str(account_number)
        )

        # Wait till 90 day radio button loads and click it
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="period_90"]'))
        ).click()

        # Ensure that transactions show after radio button click
        time.sleep(3)

        # Grab all of the transactions on the page
        transactions = driver.find_elements(
            By.XPATH, '//*[@id="content-body-full"]/table/tbody/tr'
        )

        transactions_data = []

        # For each transaction, grab the relevent transaction data
        for x in range(1, len(transactions)):
            transaction_data = {}
            transaction_data["tradeDate"] = driver.find_element(
                By.XPATH,
                '//*[@id="content-body-full"]/table/tbody/tr[' + str(x) + "]/td[1]",
            ).text
            transaction_data["settleDate"] = driver.find_element(
                By.XPATH,
                '//*[@id="content-body-full"]/table/tbody/tr[' + str(x) + "]/td[2]",
            ).text
            transaction_data["reference"] = driver.find_element(
                By.XPATH,
                '//*[@id="content-body-full"]/table/tbody/tr[' + str(x) + "]/td[3]",
            ).text
            transaction_data["description"] = driver.find_element(
                By.XPATH,
                '//*[@id="content-body-full"]/table/tbody/tr[' + str(x) + "]/td[4]",
            ).text
            transaction_data["unitCost"] = driver.find_element(
                By.XPATH,
                '//*[@id="content-body-full"]/table/tbody/tr[' + str(x) + "]/td[5]",
            ).text
            transaction_data["quantity"] = driver.find_element(
                By.XPATH,
                '//*[@id="content-body-full"]/table/tbody/tr[' + str(x) + "]/td[6]",
            ).text
            transaction_data["value"] = driver.find_element(
                By.XPATH,
                '//*[@id="content-body-full"]/table/tbody/tr[' + str(x) + "]/td[7]",
            ).text
            transactions_data.append(transaction_data)

        return transactions_data
