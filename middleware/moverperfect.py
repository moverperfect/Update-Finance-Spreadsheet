import datetime

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
        Moverperfect.__shareworks(sheet, shareworks_data)
        Moverperfect.__standard_life(standard_life_data)
        Moverperfect.__hargreaves(hargreaves_data)

    @staticmethod
    def __nutmeg(sheet: GoogleSheets, nutmeg_data):
        """
        Insert Nutmeg platform data into Google Spreadsheet.

        :param nutmeg_data: Data from the Nutmeg platform.
        """

        # Function to check if the date in a given row-1 matches the transaction_date
        def previous_date_matches(
            sheet: GoogleSheets, index: int, transaction_date: datetime
        ):
            # Read the date from the specified row
            dates = sheet.read_range("Nutmeg", f"A{index - 1}:A{index - 1}")

            # Compare the date from the sheet with the transaction_date
            return dates[0].value == transaction_date.strftime("%d/%m/%Y")

        # Initialize the starting and ending row indices
        start_row = 1
        end_row = 100

        # Find the index of the first empty row within the initial range
        empty_row_index = Moverperfect.__find_empty_row(
            sheet, "Nutmeg", start_row, end_row, "A"
        )

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = Moverperfect.__find_empty_row(
                sheet, "Nutmeg", start_row, end_row, "A"
            )

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
        empty_row_index = Moverperfect.__find_empty_row(
            sheet, "Nutmeg Monthly", start_row, end_row, "H"
        )

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = Moverperfect.__find_empty_row(
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

        SHEET_NAME = "Share Purchase Plan"

        def compare_date_1_greater_2(date_1: str, date_2: str) -> bool:
            return datetime.datetime.strptime(
                date_1, "%d/%m/%Y"
            ) > datetime.datetime.strptime(date_2, "%d/%m/%Y")

        def format_date(date_str: str) -> str:
            return datetime.datetime.strptime(date_str, "%d-%b-%Y").strftime("%d/%m/%Y")

        def insert_shareworks_transaction(
            transaction: list[str], row_index: int
        ) -> None:
            """
            Insert a single Shareworks transaction into the Google Sheet.

            :param transaction: A single Shareworks transaction as a list of strings.
            :param row_index: The row index in the Google Sheet to insert the transaction.
            """
            sheet.write_range(
                SHEET_NAME,
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
        empty_row_index = Moverperfect.__find_empty_row(
            sheet, SHEET_NAME, start_row, end_row, "A"
        )

        # Keep searching for an empty row in the next 100-row blocks until one is found
        while empty_row_index is None:
            start_row += 100
            end_row += 100
            empty_row_index = Moverperfect.__find_empty_row(
                sheet, SHEET_NAME, start_row, end_row, "A"
            )

        last_transaction_date = next(
            (
                sheet.read_cell(SHEET_NAME, f"A{search_row}")
                for search_row in range(empty_row_index, 1, -1)
                if sheet.read_cell(SHEET_NAME, f"C{search_row}") is not None
            ),
            None,
        )

        relevant_transactions = [
            transaction
            for transaction in reversed(shareworks_data["transactionData"])
            if transaction[1] == "You bought"
        ]

        for i in range(len(relevant_transactions) - 1, -1, -2):
            transaction = relevant_transactions[i]
            if (
                compare_date_1_greater_2(
                    last_transaction_date, format_date(transaction[0])
                )
                or format_date(transaction[0]) == last_transaction_date
            ):
                continue
            insert_shareworks_transaction(transaction, empty_row_index)
            empty_row_index = empty_row_index + 1

        # Iterate through rows in reverse to find the first non-empty cell in column C
        for i in range(empty_row_index - 1, 1, -1):
            if sheet.read_cell(SHEET_NAME, f"C{i}") is None:
                break

        # Define reusable expressions for formulas
        sum_formula = f"SUM(ARRAYFORMULA(G{i+1}:G{empty_row_index-1} * F{i+1}:F{empty_row_index-1}))"
        sum_previous_rows = f"SUM(E{i+1}:E{empty_row_index-1})"

        sheet.write_range(
            SHEET_NAME,
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
                f"=IF(F{empty_row_index}=0,0,({0 if (i+1) == empty_row_index else sum_previous_rows}/2)*H{empty_row_index}+J{empty_row_index})",
                f"=I{empty_row_index}/2+J{empty_row_index}/2",
            ],
        )

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

    # Function to find the index of the first empty row within a given range
    @staticmethod
    def __find_empty_row(sheet, worksheet, start_row, end_row, column):
        # Read the specified range of rows from the sheet
        dates = sheet.read_range(worksheet, f"{column}{start_row}:{column}{end_row}")

        # Iterate through the rows and find the first empty one
        for index, date in enumerate(dates):
            if date.value == "":
                return index + start_row
        return None
