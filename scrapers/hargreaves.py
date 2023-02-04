import logging
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
        accounts,
    ):
        """Initialize the instance variables for the class methods"""
        self.driver = driver
        self.username = username
        self.dob = dob
        self.password = password
        self.secure_number = secure_number
        self.accounts = accounts

    def scrape_data(self):
        """Scrape transaction and portfolio data from the Hargreaves Lansdown website"""
        try:
            # Use the driver instance
            with self.driver as driver:
                self.__login(driver)

                # Return the data as a dictionary
                return ""
        except Exception as exception:
            logging.error(exception)
            return {
                "transactionDate": 0,
                "netContributions": 0,
                "currentValue": 0,
            }

    def __login(self, driver):
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

        wait.until(
            EC.element_to_be_clickable((By.ID, "online-password-verification"))
        ).send_keys(self.password)

        secret_number_elements = driver.find_elements(
            By.XPATH, '//div[@class="secure-number-container__label"]'
        )

        for x in range(0, len(secret_number_elements)):
            label = secret_number_elements[x].text[:1]
            driver.find_element(
                By.XPATH,
                '//div[@class="secure-number-container__label"]['
                + str(x + 1)
                + "]/div/input",
            ).send_keys(self.secure_number[int(label) - 1])

        wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="submit"]',
                )
            )
        ).click()

        # Wait until page loads
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="breadcrumbs"]/div[1]/strong[1]')
            )
        )
