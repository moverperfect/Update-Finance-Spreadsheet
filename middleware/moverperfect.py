from connectors.gsheet import GoogleSheets


class Moverperfect:
    """
    A class to handle the insertion of data from various investment platforms.
    """

    @staticmethod
    def insert_all(
        secrets, nutmeg_data, shareworks_data, standard_life_data, hargreaves_data
    ):
        """
        Insert data from all investment platforms into Google Spreadsheet.

        :param nutmeg_data: Data from the Nutmeg platform.
        :param shareworks_data: Data from the Shareworks platform.
        :param standard_life_data: Data from the Standard Life platform.
        :param hargreaves_data: Data from the Hargreaves Lansdown platform.
        """
        sheet = GoogleSheets(secrets["SHEET_ID"])

        Moverperfect.__nutmeg(sheet, nutmeg_data)
        Moverperfect.__shareworks(shareworks_data)
        Moverperfect.__standard_life(standard_life_data)
        Moverperfect.__hargreaves(hargreaves_data)

    @staticmethod
    def __nutmeg(sheet: GoogleSheets, nutmeg_data):
        """
        Insert Nutmeg platform data into Google Spreadsheet.

        :param nutmeg_data: Data from the Nutmeg platform.
        """

        # Function to find the index of the first empty row within a given range
        def find_empty_row(sheet, worksheet, start_row, end_row, column):
            # Read the specified range of rows from the sheet
            dates = sheet.read_range(
                worksheet, f"{column}{start_row}:{column}{end_row}"
            )

            # Iterate through the rows and find the first empty one
            for index, date in enumerate(dates):
                if date.value == "":
                    return index + start_row
            return None

        # Function to check if the date in a given row-1 matches the transaction_date
        def previous_date_matches(sheet, index, transaction_date):
            # Read the date from the specified row
            dates = sheet.read_range("Nutmeg", f"A{index - 1}:A{index - 1}")

            # Compare the date from the sheet with the transaction_date
            return dates[0].value == transaction_date.strftime("%d/%m/%Y")

        # Initialize the starting and ending row indices
        start_row = 1
        end_row = 100

        # Find the index of the first empty row within the initial range
        empty_row_index = find_empty_row(sheet, "Nutmeg", start_row, end_row, "A")

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = find_empty_row(sheet, "Nutmeg", start_row, end_row, "A")

        # Iterate through the transactions in reversed(ascending) order
        for i, transaction in enumerate(reversed(nutmeg_data["transactions"])):
            # If the date of the current transaction matches the date in the sheet
            if previous_date_matches(sheet, empty_row_index, transaction["date"]):
                # Iterate through the transactions in reversed(asc) order inserting them
                for previous_transaction in reversed(
                    nutmeg_data["transactions"][: len(nutmeg_data["transactions"]) - i]
                ):
                    # Skip transaction if it already exists in the sheet
                    if previous_date_matches(
                        sheet, empty_row_index, previous_transaction["date"]
                    ):
                        continue

                    # Write the transaction data to the sheet
                    sheet.write_range(
                        "Nutmeg",
                        f"A{empty_row_index}:F{empty_row_index}",
                        [
                            previous_transaction["date"].strftime("%d/%m/%Y"),
                            previous_transaction["transaction"],
                            previous_transaction["pot"],
                            previous_transaction["amount"],
                            "",
                            f"=F{empty_row_index - 1}+D{empty_row_index}",
                        ],
                    )
                    # Move to the next row
                    empty_row_index += 1
                break

        # Initialize the starting and ending row indices
        start_row = 1
        end_row = 100

        # Find the index of the first empty row within the initial range
        empty_row_index = find_empty_row(
            sheet, "Nutmeg Monthly", start_row, end_row, "H"
        )

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = find_empty_row(
                sheet, "Nutmeg Monthly", start_row, end_row, "H"
            )

        # Write latest data
        sheet.write_range(
            "Nutmeg Monthly",
            f"H{empty_row_index}:I{empty_row_index}",
            [nutmeg_data["netContributions"], nutmeg_data["currentValue"]],
        )

    @staticmethod
    def __shareworks(shareworks_data):
        """
        Insert Shareworks platform data into Google Spreadsheet.

        :param shareworks_data: Data from the Shareworks platform.
        """
        return

    @staticmethod
    def __standard_life(standard_life_data):
        """
        Insert Standard Life platform data into Google Spreadsheet.

        :param standard_life_data: Data from the Standard Life platform.
        """
        return

    @staticmethod
    def __hargreaves(hargreaves_data):
        """
        Insert Hargreaves Lansdown platform data into Google Spreadsheet.

        :param hargreaves_data: Data from the Hargreaves Lansdown platform.
        """
        return
