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

    def read_cell(self, worksheet_name, cell_address):
        """Read the value of a cell in a worksheet"""
        # Open the sheet using its key
        with self.client.open_by_key(self.spreadsheet_id) as sheet:
            # Get the worksheet by name
            worksheet = sheet.worksheet(worksheet_name)
            # Get the cell by address
            cell = worksheet.acell(cell_address)
            # Return the cell value
            return cell.value

    def write_cell(self, worksheet_name, cell_address, value):
        """Write a value to a cell in a worksheet"""
        # Open the sheet using its key
        with self.client.open_by_key(self.spreadsheet_id) as sheet:
            # Get the worksheet by name
            worksheet = sheet.worksheet(worksheet_name)
            # Update the cell value
            worksheet.update_acell(cell_address, value)

    def read_range(self, worksheet_name, range_address):
        """Read the values of a range of cells in a worksheet"""
        # Open the sheet using its key
        with self.client.open_by_key(self.spreadsheet_id) as sheet:
            # Get the worksheet by name
            worksheet = sheet.worksheet(worksheet_name)
            # Get the range of cells
            cells = worksheet.range(range_address)
            # Return the values of the cells as a list
            return [cell.value for cell in cells]

    def write_range(self, worksheet_name, range_address, values):
        """Write values to a range of cells in a worksheet"""
        # Open the sheet using its key
        with self.client.open_by_key(self.spreadsheet_id) as sheet:
            # Get the worksheet by name
            worksheet = sheet.worksheet(worksheet_name)
            # Get the range of cells
            cells = worksheet.range(range_address)
            # Update the values of the cells
            for cell, value in zip(cells, values):
                cell.value = value
            worksheet.update_cells(cells)
