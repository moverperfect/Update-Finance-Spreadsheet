import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time


class ShareWorks:
    """A class for scraping data from the Shareworks website"""

    def __init__(self, driver: webdriver.Chrome, host, username, passwd):
        """Initialize the instance variables for the class methods"""
        self.driver: webdriver.Chrome = driver
        self.host = host
        self.username = username
        self.passwd = passwd

    def scrape_data(self):
        """Scrape transaction and portfolio data from the Shareworks website"""
        try:
            # Use the driver instance
            with self.driver as driver:
                # Navigate to the login page
                driver.get("https://" + self.host + "/solium/servlet/userLogin.do")

                wait = WebDriverWait(driver, 60)

                time.sleep(2)

                # Enter the email and password
                wait.until(
                    EC.element_to_be_clickable((By.ID, "account_number_input"))
                ).send_keys(self.username)

                time.sleep(2)

                wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(
                    self.passwd
                )

                time.sleep(5)

                # Submit the form
                wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="submit-box"]/input',
                        )
                    )
                ).click()

                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="hero-total-portfolio-value"]/span/span[2]')
                    )
                )

                # Navigae to the transaction history page
                # driver.get(
                #     "https://"
                #     + self.host
                #     + "/solium/servlet/ui/activity/reports/statement"
                # )

                time.sleep(2)

                wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="main-navigation-item-activity"]/a/div/div[2]',
                        )
                    )
                ).click()
                time.sleep(2)
                wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="App_sticky_sub_nav"]/ul/li[2]/a')
                    )
                ).click()

                iframe = driver.find_element(
                    By.XPATH, '//*[@id="transaction-statement-iframe"]'
                )
                driver.switch_to.frame(iframe)
                time.sleep(2)
                submit = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="submit_html"]'))
                )

                # start_date = driver.find_element(By.XPATH, '//*[@id="start_date"]')
                # start_date.clear()
                # start_date.send_keys(
                #     (datetime.now() - timedelta(days=31)).strftime("%Y-%m-%d")
                # )
                drp_date_select: Select = Select(
                    driver.find_element(By.XPATH, '//*[@id="date_select"]')
                )
                drp_date_select.select_by_visible_text("All Available History")
                time.sleep(1)
                submit.click()

                rows = driver.find_elements(
                    By.XPATH, '//*[@id="Activity_table"]/tbody/tr'
                )

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

                driver.switch_to.default_content()

                # Navigate to the portfolio page
                driver.get(
                    "https://" + self.host + "/solium/servlet/ui/portfolio/holdings"
                )

                iframe = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="portfolio-holdings-iframe"]')
                    )
                )

                driver.switch_to.frame(iframe)
                time.sleep(1)
                drp_display_currency: Select = Select(
                    driver.find_element(By.XPATH, '//*[@id="display_currency"]')
                )
                drp_display_currency.select_by_visible_text("British Pounds Sterling")

                exchange_rate = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="exchangeRateTable"]/tbody/tr[2]/td[3]')
                    )
                ).text.split(" ")[0]

                current_value = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="Transaction View of International Purchase Plan_table"]/tbody/tr[5]/td[3]',
                        )
                    )
                ).text

                total_shares = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="Transaction View of International Purchase Plan_table"]/tbody/tr[4]/td[4]',
                        )
                    )
                ).text

                driver.switch_to.default_content()

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
