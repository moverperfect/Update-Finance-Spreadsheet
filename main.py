from selenium import webdriver
from scrapers.nutmeg import Nutmeg
from scrapers.shareworks import ShareWorks
from utils.secrets import read_secrets
from selenium.webdriver.chrome.options import Options as ChromeOptions

if __name__ == "__main__":
    secrets = read_secrets()

    options = ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    nutmeg = Nutmeg(driver, secrets["NUTMEG_EMAIL"], secrets["NUTMEG_PASSWORD"])

    data = nutmeg.scrape_data()

    shareworks = ShareWorks(
        driver,
        secrets["SHAREWORKS_HOST"],
        secrets["SHAREWORKS_USERNAME"],
        secrets["SHAREWORKS_PASSWORD"],
    )

    data = shareworks.scrape_data()

    print(data)
