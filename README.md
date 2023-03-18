# Update Finance Spreadsheet

![GitHub last commit](https://img.shields.io/github/last-commit/moverperfect/Update-Finance-Spreadsheet?label=last%20activity)
![GitHub issues](https://img.shields.io/github/issues-raw/moverperfect/Update-Finance-Spreadsheet)
[![MegaLinter](https://github.com/moverperfect/Update-Finance-Spreadsheet/workflows/MegaLinter/badge.svg?branch=main)](https://github.com/moverperfect/Update-Finance-Spreadsheet/actions?query=workflow%3AMegaLinter+branch%3Amain)
![GitHub](https://img.shields.io/github/license/moverperfect/Update-Finance-Spreadsheet)

Update Finance Spreadsheet is a Python-based personal project that automatically scrapes financial account information from various websites and updates the data in Google Sheets and YNAB (You Need a Budget) accounts.

## Features

- Scrapes financial account information from multiple websites:
  - Hargreaves Lansdown
  - Nutmeg
  - Shareworks
  - StandardLife
- Inserts scraped data into Google Sheets and YNAB accounts
- Automated updates with Python Selenium scrapers
- Utilizes gspread, selenium, and webdriver_manager libraries
- Includes GitHub Actions for Dependabot, MegaLinter, and CodeQL

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)

### Configuration

Create a `secrets.json` file in the root directory of the project with your credentials and settings for the financial websites and Google Sheets. Use the following format, replacing the example values with your actual credentials:

```json
{
  "NUTMEG_EMAIL": "example@example.com",
  "NUTMEG_PASSWORD": "Password",
  "SHAREWORKS_USERNAME": "Username",
  "SHAREWORKS_PASSWORD": "Password",
  "SHAREWORKS_HOST": "example.com",
  "HARGREAVES_USERNAME": "Username",
  "HARGREAVES_DOB": "DD/MM/YY",
  "HARGREAVES_PASSWORD": "Password",
  "HARGREAVES_SECRET_NUMBER": "123456",
  "HARGREAVES_ACCOUNTS": ["01", "02"],
  "STANDARDLIFE_USERNAME": "Username",
  "STANDARDLIFE_PASSWORD": "Password",
  "SHEET_ID": "GOOGLE_SHEET_ID"
}
```

_Note: Make sure not to commit the secrets.json file to your repository, as it contains sensitive information. Add it to your .gitignore file._

### Installation

1. Clone the repository:

```
git clone https://github.com/moverperfect/Update-Finance-Spreadsheet.git
```

2. Change to the project directory:

```
cd Update-Finance-Spreadsheet
```

3. Install the required packages:

```
pip install -r requirements.txt
```

4. Update the `secrets.json` file as shown above with your credentials and settings for the financial websites, Google Sheets, and YNAB accounts.

5. Run the `Main.py` script to start the scraping process:

```
python Main.py
```

## Project Structure

The project is organized into the following folders and files:

- `Main.py`: Entrypoint for the program, initiates the scraping process.
- `scrapers/`: Contains Python Selenium scrapers for each supported financial website.
- `utils/`: Contains the code to grab the secrets from the `secrets.json`.
- `connectors/`: Contains the API code to interact with Google Sheets and YNAB.
- `middleware/`: Contains the code that translates the scraper information into commands to insert the data into the API code in Google Sheets.
- `requirements.txt`: Lists the Python libraries required for the project.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Built With

- [Python](https://www.python.org/)
- [Selenium](https://selenium-python.readthedocs.io/)
- [gspread](https://gspread.readthedocs.io/en/latest/)
- [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)

## GitHub Actions

- [Dependabot](https://github.com/dependabot/dependabot-core)
- [MegaLinter](https://megalinter.io/latest/)
- [CodeQL](https://codeql.github.com/)

## Author

[moverperfect](https://github.com/moverperfect)
