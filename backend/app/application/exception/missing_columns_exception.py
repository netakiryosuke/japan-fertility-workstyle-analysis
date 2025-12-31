class MissingColumnsException(Exception):
    def __init__(self, missing_columns: list[str]):
        self.missing_columns = missing_columns
        super().__init__(f"Required columns are missing in CSV file: {missing_columns}")
