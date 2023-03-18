import logging
import time
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

PENSION_SUMMARY_TAB = (
    '//*[@id="tab-summary"]/tcs-pensions-summary-tab/tcs-view-plan-summary-pension'
)


class StandardLife:
    """A class for scraping data from the Standard Life website"""

    def __init__(self, username: str, passwd: str):
        """Initialize the instance variables for the class methods"""
        self.username = username
        self.passwd = passwd

    def scrape_data(self, driver: WebDriver) -> dict[str, Any]:
        """Scrape transaction and portfolio data from the Standard Life website"""
        try:
            # Set up wait and log in to Standard Life
            wait = WebDriverWait(driver, 60)
            self.__login(driver, wait)

            time.sleep(5)

            accept_cookie = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="cookieAcceptAllLink"]'))
            )

            time.sleep(5)

            accept_cookie.click()

            # Naviagate to portfolio page and change dropdown to GBP
            wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/app-root/app-secure-container/tcs-main-nav/div"
                        + "/mat-sidenav-container/mat-sidenav-content/tcs-dashboard"
                        + "/div[2]/div[2]/tcs-hero-tile/div/a",
                    )
                )
            ).click()

            time.sleep(5)

            # Grab exchange rate, current value, and total shares
            total_payments = self.__get_total_payments(wait)
            investment_growth = self.__get_investment_growth(wait)
            total_value = self.__get_total_value(wait)

            # Grab transaction data
            transaction_data = self.__get_transaction_data(driver, wait)

            # Return the data as a dictionary
            return {
                "transactionData": transaction_data,
                "totalPayments": total_payments,
                "investmentGrowth": investment_growth,
                "totalValue": total_value,
            }
        except Exception as exception:
            logging.error(exception)
            return {
                "transactionData": 0,
                "totalPayments": 0,
                "investmentGrowth": 0,
                "totalValue": 0,
            }

    def __login(self, driver: WebDriver, wait: WebDriverWait):
        """Log into the website on the driver"""
        # Navigate to the login page
        driver.get(
            "https://online.standardlife.com"
            + "/secure/customer-authentication-client/customer/login"
        )

        # Enter the email and password
        wait.until(EC.element_to_be_clickable((By.ID, "userid"))).send_keys(
            self.username
        )

        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(
            self.passwd
        )

        # Submit the form
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "submit",
                )
            )
        ).click()

    def __get_total_payments(self, wait: WebDriverWait) -> str:
        """Return the current exchange rate shown on the portfolio page"""
        return wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    PENSION_SUMMARY_TAB + "/div[2]/div[1]/div/p",
                )
            )
        ).text

    def __get_investment_growth(self, wait: WebDriverWait) -> str:
        """Return the current exchange rate shown on the portfolio page"""
        return wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    PENSION_SUMMARY_TAB + "/div[2]/div[3]/div/p",
                )
            )
        ).text

    def __get_total_value(self, wait: WebDriverWait) -> str:
        """Return the current exchange rate shown on the portfolio page"""
        return wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    PENSION_SUMMARY_TAB + "/div[2]/div[4]/div/p",
                )
            )
        ).text

    def __get_transaction_data(self, driver: WebDriver, wait: WebDriverWait) -> list:
        """Open the transaction page, select all history from dropdown
        and collect all transaction history"""
        # Select the Activity Page
        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="mat-tab-label-0-2"]/div',
                )
            )
        ).click()

        time.sleep(1)

        # Grab all of the rows in the activity table
        rows = driver.find_elements(
            By.XPATH,
            '//*[@id="tab-transaction"]/tcs-transaction-tab'
            + "/div[2]/tcs-transaction-history/div[3]"
            + "/table/tbody/tr",
        )
        transaction_data = []

        # Iterate over the rows
        for row in rows:
            # Find all the cells in the row
            cells = row.find_elements(By.XPATH, ".//td")

            # Initialize a list to store the data for this row
            row_data = []

            # Iterate over the cells
            for cell in cells:
                if cell.text == "" and cell.accessible_name == "":
                    continue
                # Extract the text from the cell and append it to the row data
                row_data.append(cell.accessible_name if cell.text == "" else cell.text)

            # Append the row data to the 2D array
            transaction_data.append(row_data)

        # Return the transaction data
        return transaction_data
