from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from scrapers.hargreaves import Hargreaves
from scrapers.nutmeg import Nutmeg
from scrapers.shareworks import ShareWorks
from scrapers.standardlife import StandardLife
from utils.secrets import read_secrets

if __name__ == "__main__":
    secrets = read_secrets()

    options = ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    nutmeg = Nutmeg(secrets["NUTMEG_EMAIL"], secrets["NUTMEG_PASSWORD"])

    nutmeg_data = nutmeg.scrape_data(driver)

    print(nutmeg_data)

    shareworks = ShareWorks(
        secrets["SHAREWORKS_HOST"],
        secrets["SHAREWORKS_USERNAME"],
        secrets["SHAREWORKS_PASSWORD"],
    )

    shareworks_data = shareworks.scrape_data(driver)

    print(shareworks_data)

    standard_life = StandardLife(
        secrets["STANDARDLIFE_USERNAME"], secrets["STANDARDLIFE_PASSWORD"]
    )

    standard_life_data = standard_life.scrape_data(driver)

    print(standard_life_data)

    hargreaves = Hargreaves(
        secrets["HARGREAVES_USERNAME"],
        secrets["HARGREAVES_DOB"],
        secrets["HARGREAVES_PASSWORD"],
        secrets["HARGREAVES_SECRET_NUMBER"],
        secrets["HARGREAVES_ACCOUNTS"],
    )

    hargreaves_data = hargreaves.scrape_data(driver)

    print(hargreaves_data)

    print("Finished")
