import datetime

from connectors.gsheet import GoogleSheets


class Moverperfect:
    """
    A class to handle the insertion of data from various investment platforms.
    """

    @staticmethod
    def insert_all(secrets, nutmeg_data, shareworks_data, standard_life_data):
        """
        Insert data from all investment platforms into Google Spreadsheet.

        :param nutmeg_data: Data from the Nutmeg platform.
        :param shareworks_data: Data from the Shareworks platform.
        :param standard_life_data: Data from the Standard Life platform.
        :param hargreaves_data: Data from the Hargreaves Lansdown platform.
        """
        sheet = GoogleSheets(secrets["SHEET_ID"])

        Moverperfect.__nutmeg(sheet, nutmeg_data)
        Moverperfect.__shareworks(sheet, shareworks_data)
        Moverperfect.__standard_life(sheet, standard_life_data)
        # Moverperfect.__hargreaves(hargreaves_data)

    @staticmethod
    def __nutmeg(sheet: GoogleSheets, nutmeg_data):
        """
        Insert Nutmeg platform data into Google Spreadsheet.

        :param nutmeg_data: Data from the Nutmeg platform.
        """

        # Function to check if the date in a given row-1 matches the transaction_date
        def previous_date_matches(
            sheet: GoogleSheets, index: int, transaction_date: datetime.datetime
        ):
            # Read the date from the specified row
            dates = sheet.read_range("Nutmeg", f"A{index - 1}:A{index - 1}")

            # Compare the date from the sheet with the transaction_date
            return dates[0].value == transaction_date.strftime("%d/%m/%Y")

        # Initialize the starting and ending row indices
        start_row = 1
        end_row = 100

        # Find the index of the first empty row within the initial range
        empty_row_index = __find_empty_row(sheet, "Nutmeg", start_row, end_row, "A")

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = __find_empty_row(sheet, "Nutmeg", start_row, end_row, "A")

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
        empty_row_index = __find_empty_row(
            sheet, "Nutmeg Monthly", start_row, end_row, "H"
        )

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = __find_empty_row(
                sheet, "Nutmeg Monthly", start_row, end_row, "H"
            )

        # Write latest data
        sheet.write_range(
            "Nutmeg Monthly",
            f"H{empty_row_index}:I{empty_row_index}",
            [nutmeg_data["netContributions"], nutmeg_data["currentValue"]],
        )

    @staticmethod
    def __shareworks(sheet: GoogleSheets, shareworks_data):
        """
        Insert Shareworks platform data into Google Spreadsheet.

        :param shareworks_data: Data from the Shareworks platform.
        """

        sheet_name = "Share Purchase Plan"

        def format_date(date_str: str) -> str:
            return datetime.datetime.strptime(date_str, "%d-%b-%Y").strftime("%d/%m/%Y")

        def insert_shareworks_transaction(
            transaction: list[str], row_index: int
        ) -> None:
            """
            Insert a single Shareworks transaction into the Google Sheet.

            :param transaction: A single Shareworks transaction as a list of strings.
            :param row_index: The row index in the Google Sheet to insert the
            transaction.
            """
            sheet.write_range(
                sheet_name,
                f"A{row_index}:M{row_index}",
                [
                    formatted_date := format_date(transaction[0]),
                    formatted_date,
                    "PAYROLL PURCHASE",
                    formatted_value := transaction[5].replace("$", ""),
                    f"={transaction[6].replace('$', '')}*2",
                    formatted_value,
                    f"={transaction[4]}*2",
                    "",
                    "=NA()",
                    "=NA()",
                    "=NA()",
                    "=NA()",
                    "=NA()",
                ],
            )

        # Initialize the starting and ending row indices
        start_row = 1
        end_row = 100

        # Find the index of the first empty row within the initial range
        empty_row_index = __find_empty_row(sheet, sheet_name, start_row, end_row, "A")

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = __find_empty_row(
                sheet, sheet_name, start_row, end_row, "A"
            )

        last_transaction_date = next(
            (
                sheet.read_cell(sheet_name, f"A{search_row}")
                for search_row in range(empty_row_index, 1, -1)
                if sheet.read_cell(sheet_name, f"C{search_row}") is not None
            ),
            "01/01/1970",
        )

        relevant_transactions = [
            transaction
            for transaction in reversed(shareworks_data["transactionData"])
            if transaction[1] == "You bought"
        ]

        for i in range(len(relevant_transactions) - 1, -1, -2):
            transaction = relevant_transactions[i]
            if (
                __compare_date_1_greater_2(
                    last_transaction_date, format_date(transaction[0])
                )
                or format_date(transaction[0]) == last_transaction_date
            ):
                continue
            insert_shareworks_transaction(transaction, empty_row_index)
            empty_row_index = empty_row_index + 1

        i = empty_row_index - 1
        # Iterate through rows in reverse to find the first non-empty cell in column C
        for i in range(empty_row_index - 1, 1, -1):
            if sheet.read_cell(sheet_name, f"C{i}") is None:
                break

        # Define reusable expressions for formulas
        sum_formula = (
            f"SUM(ARRAYFORMULA(G{i+1}:G{empty_row_index-1} "
            + f"* F{i+1}:F{empty_row_index-1}))"
        )
        sum_previous_rows = f"SUM(E{i+1}:E{empty_row_index-1})"

        sheet.write_range(
            sheet_name,
            f"A{empty_row_index}:M{empty_row_index}",
            [
                datetime.datetime.now().strftime("%d/%m/%Y"),
                datetime.datetime.now().strftime("%d/%m/%Y"),
                "",
                "",
                "",
                shareworks_data["sharePrice"].replace("$", ""),
                f"=SUM(G{i}:G{empty_row_index - 1})",
                shareworks_data["exchangeRate"],
                f"=(F{empty_row_index}*G{empty_row_index})*H{empty_row_index}",
                # Previous Calculated Return +
                # (((New Number of Shares * Current Stock Price) -
                # (Previous Number of Shares * Previous Stock Price)) -
                # (Number of Shares Purchased * Purchase Price)) *
                # (USD/GBP Exchange Rate)
                f"=IF(H{empty_row_index}=0,0,J{i} + "
                + f"((G{empty_row_index} * F{empty_row_index}) - "
                + f"(G{i} * F{i}) - "
                + f"({0 if (i+1) == empty_row_index else sum_formula})) * "
                + f"H{empty_row_index})",
                f"=J{empty_row_index}/I{empty_row_index}",
                # (Purchase amount in $/2) *
                # Exchange Rate+Return in £
                f"=IF(F{empty_row_index}=0,0,("
                + f"{0 if (i+1) == empty_row_index else sum_previous_rows}/2)"
                + f"*H{empty_row_index}+J{empty_row_index})",
                f"=I{empty_row_index}/2+J{empty_row_index}/2",
            ],
        )

    @staticmethod
    def __standard_life(sheet: GoogleSheets, standard_life_data):
        """
        Insert Standard Life platform data into Google Spreadsheet.

        :param standard_life_data: Data from the Standard Life platform.
        """

        def insert_standardlife_transaction(
            transaction: list[str], row_index: int
        ) -> None:
            """
            Insert a single Standard Life transaction into the Google Sheet.

            :param transaction: A single Standard Life transaction as a list of strings.
            :param row_index: The row index in the Google Sheet to insert the
            transaction.
            """
            sheet.write_range(
                sheet_name,
                f"A{row_index}:C{row_index}",
                [
                    transaction[1],
                    transaction[2].replace("£", ""),
                    transaction[2].replace("£", ""),
                ],
            )

        sheet_name = "Pension"

        # Initialize the starting and ending row indices
        start_row = 1
        end_row = 100

        # Find the index of the first empty row within the initial range
        empty_row_index = __find_empty_row(sheet, sheet_name, start_row, end_row, "A")

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = __find_empty_row(
                sheet, sheet_name, start_row, end_row, "A"
            )

        last_transaction_date = next(
            (
                sheet.read_cell(sheet_name, f"A{search_row}")
                for search_row in range(empty_row_index, 1, -1)
                if sheet.read_cell(sheet_name, f"B{search_row}") is not None
            ),
            "01/01/1970",
        )

        # Insert new transactions
        for i in range(len(standard_life_data["transactionData"]) - 1, -1, -1):
            transaction = standard_life_data["transactionData"][i]
            if (
                __compare_date_1_greater_2(last_transaction_date, transaction[1])
                or transaction[1] == last_transaction_date
            ):
                continue
            insert_standardlife_transaction(transaction, empty_row_index)
            empty_row_index = empty_row_index + 1

        # Insert latest valuation
        sheet.write_range(
            sheet_name,
            f"A{empty_row_index}:G{empty_row_index}",
            [
                datetime.datetime.now().strftime("%d/%m/%Y"),
                "",
                "",
                standard_life_data["totalPayments"],
                standard_life_data["investmentGrowth"],
                f"=E{empty_row_index}/D{empty_row_index}",
                f"=D{empty_row_index}+E{empty_row_index}",
            ],
        )

    # @staticmethod
    # def __hargreaves(hargreaves_data):
    #     """
    #     Insert Hargreaves Lansdown platform data into Google Spreadsheet.

    #     :param hargreaves_data: Data from the Hargreaves Lansdown platform.
    #     """
    #     return


def __find_empty_row(
    sheet: GoogleSheets, worksheet: str, start_row: int, end_row: int, column: str
) -> int | None:
    """
    Find the first empty row within a specified range in a Google Sheet.

    :param sheet: The Google Sheet instance.
    :param worksheet: The name of the worksheet to search.
    :param start_row: The starting row index to search.
    :param end_row: The ending row index to search.
    :param column: The column letter to search for an empty row.
    :return: The index of the first empty row, or None if no empty row is found.
    """

    # Read the specified range of rows from the sheet
    dates = sheet.read_range(worksheet, f"{column}{start_row}:{column}{end_row}")

    # Iterate through the rows and find the first empty one
    for index, date in enumerate(dates):
        if date.value == "":
            return index + start_row
    return None


def __compare_date_1_greater_2(date_1: str, date_2: str) -> bool:
    """
    Compare two date strings and return True if date_1 is greater than date_2.

    :param date_1: The first date string in the format "%d/%m/%Y".
    :param date_2: The second date string in the format "%d/%m/%Y".
    :return: True if date_1 is greater than date_2, False otherwise.
    """

    return datetime.datetime.strptime(date_1, "%d/%m/%Y") > datetime.datetime.strptime(
        date_2, "%d/%m/%Y"
    )
