from backend.app.infrastructure.csv_dataframe_loader import CsvDataFrameLoader

def get_csv_dataframe_loader() -> CsvDataFrameLoader:
    return CsvDataFrameLoader()
