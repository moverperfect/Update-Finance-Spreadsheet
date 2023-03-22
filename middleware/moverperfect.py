class Moverperfect:
    """
    A class to handle the insertion of data from various investment platforms.
    """

    @staticmethod
    def insert_all(nutmeg_data, shareworks_data, standard_life_data, hargreaves_data):
        """
        Insert data from all investment platforms into Google Spreadsheet.

        :param nutmeg_data: Data from the Nutmeg platform.
        :param shareworks_data: Data from the Shareworks platform.
        :param standard_life_data: Data from the Standard Life platform.
        :param hargreaves_data: Data from the Hargreaves Lansdown platform.
        """
        Moverperfect.__nutmeg(nutmeg_data)
        Moverperfect.__shareworks(shareworks_data)
        Moverperfect.__standard_life(standard_life_data)
        Moverperfect.__hargreaves(hargreaves_data)

    @staticmethod
    def __nutmeg(nutmeg_data):
        """
        Insert Nutmeg platform data into Google Spreadsheet.

        :param nutmeg_data: Data from the Nutmeg platform.
        """
        return

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
