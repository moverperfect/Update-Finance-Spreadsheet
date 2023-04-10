# pylint: disable=E1129
import gspread


class GoogleSheets:
    """A class for read/writing data to a Google Sheet"""

    def __init__(self, spreadsheet_id):
        """Initialize the class with a given spreadsheet_id"""
        self.spreadsheet_id = spreadsheet_id

        # Authorize the gspread client using credentials and authorized user files
        self.client = gspread.oauth(
            credentials_filename="./credentials.json",
            authorized_user_filename="./authorized_user.json",
        )

        # Open the sheet using its key
        self.sheet = self.client.open_by_key(self.spreadsheet_id)

    def read_cell(self, worksheet_name, cell_address):
        """Read the value of a cell in a worksheet"""

        # Get the worksheet by name
        worksheet = self.sheet.worksheet(worksheet_name)
        # Get the cell by address
        cell = worksheet.acell(cell_address)
        # Return the cell value
        return cell.value

    def write_cell(self, worksheet_name, cell_address, value):
        """Write a value to a cell in a worksheet"""

        # Get the worksheet by name
        worksheet = self.sheet.worksheet(worksheet_name)
        # Update the cell value
        worksheet.update_acell(cell_address, value)

    def read_range(self, worksheet_name, range_address):
        """Read the values of a range of cells in a worksheet"""

        # Get the worksheet by name
        worksheet = self.sheet.worksheet(worksheet_name)

        # Get the range of cells
        cells = worksheet.range(range_address)

        # Return the values of the cells as a list
        return cells

    def write_range(self, worksheet_name, range_address, values):
        """Write values to a range of cells in a worksheet"""

        # Get the worksheet by name
        worksheet = self.sheet.worksheet(worksheet_name)

        # Calculate dimensions of the range
        start_cell, end_cell = range_address.split(":")
        start_row, start_col = gspread.utils.a1_to_rowcol(start_cell)
        end_row, end_col = gspread.utils.a1_to_rowcol(end_cell)

        num_rows = end_row - start_row + 1
        num_cols = end_col - start_col + 1

        # Create a 2D list from the input values
        values_2d = [values[i : i + num_cols] for i in range(0, len(values), num_cols)]

        # Verify if the dimensions match
        if len(values_2d) != num_rows or len(values_2d[0]) != num_cols:
            raise ValueError(
                "The dimensions of the input values do not match "
                + "the dimensions of the range"
            )

        # Update the values of the cells
        worksheet.update(range_address, values_2d, value_input_option="USER_ENTERED")
