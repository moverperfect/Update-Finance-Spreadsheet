from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from scrapers.nutmeg import Nutmeg
from scrapers.shareworks import ShareWorks
from scrapers.standardlife import StandardLife
from utils.secrets import read_secrets

if __name__ == "__main__":
    secrets = read_secrets()

    options = ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    nutmeg = Nutmeg(driver, secrets["NUTMEG_EMAIL"], secrets["NUTMEG_PASSWORD"])

    print(nutmeg.scrape_data())

    shareworks = ShareWorks(
        driver,
        secrets["SHAREWORKS_HOST"],
        secrets["SHAREWORKS_USERNAME"],
        secrets["SHAREWORKS_PASSWORD"],
    )

    print(shareworks.scrape_data())

    standard_life = StandardLife(
        secrets["STANDARDLIFE_USERNAME"], secrets["STANDARDLIFE_PASSWORD"]
    )

    data = standard_life.scrape_data(driver)

    print(data)
