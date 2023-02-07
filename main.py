from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.nutmeg import Nutmeg
from scrapers.shareworks import ShareWorks
from utils.secrets import read_secrets

# from connectors.gsheet import GoogleSheets

if __name__ == "__main__":
    # sheet = GoogleSheets(secrets["SHEET_ID"])
    # print(sheet.read_cell("Main", "A1"))
    # print(sheet.read_range("Main", "A1:C5"))
    # sheet.write_cell("Main", "A1", "Changed")
    # sheet.write_range("Main", "A2:B3", ["1", "2", "3", "4"])

    secrets = read_secrets()

    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    nutmeg = Nutmeg(driver, secrets["NUTMEG_EMAIL"], secrets["NUTMEG_PASSWORD"])

    data = nutmeg.scrape_data()

    # shareworks = ShareWorks(
    #     driver,
    #     secrets["SHAREWORKS_HOST"],
    #     secrets["SHAREWORKS_USERNAME"],
    #     secrets["SHAREWORKS_PASSWORD"],
    # )

    # data = shareworks.scrape_data()

    print(data)
