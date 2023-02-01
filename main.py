from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from scrapers.nutmeg import *
from utils.secrets import read_secrets

if __name__ == "__main__":
    secrets = read_secrets()

    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(executable_path=service.path)

    nutmeg = Nutmeg(driver, secrets.NUTMEG_EMAIL, secrets.NUTMEG_PASSWORD)

    data = nutmeg.ScrapeData()

    print(data)