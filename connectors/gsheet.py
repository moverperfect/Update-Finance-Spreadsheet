import gspread


class GoogleSheets:
    # Initialize the class with a given spreadsheet_id
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id

        # Authorize the gspread client using credentials and authorized user files
        self.client = gspread.oauth(
            credentials_filename="./credentials.json",
            authorized_user_filename="./authorized_user.json",
        )

    # Read the value of a cell in a worksheet
    def read_cell(self, worksheet_name, cell_address):
        # Open the sheet using its key
        with self.client.open_by_key(self.spreadsheet_id) as sheet:
            # Get the worksheet by name
            worksheet = sheet.worksheet(worksheet_name)
            # Get the cell by address
            cell = worksheet.acell(cell_address)
            # Return the cell value
            return cell.value

    # Write a value to a cell in a worksheet
    def write_cell(self, worksheet_name, cell_address, value):
        # Open the sheet using its key
        with self.client.open_by_key(self.spreadsheet_id) as sheet:
            # Get the worksheet by name
            worksheet = sheet.worksheet(worksheet_name)
            # Update the cell value
            worksheet.update_acell(cell_address, value)

    # Read the values of a range of cells in a worksheet
    def read_range(self, worksheet_name, range_address):
        # Open the sheet using its key
        with self.client.open_by_key(self.spreadsheet_id) as sheet:
            # Get the worksheet by name
            worksheet = sheet.worksheet(worksheet_name)
            # Get the range of cells
            cells = worksheet.range(range_address)
            # Return the values of the cells as a list
            return [cell.value for cell in cells]

    # Write values to a range of cells in a worksheet
    def write_range(self, worksheet_name, range_address, values):
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
