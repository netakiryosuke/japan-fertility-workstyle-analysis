from app.infrastructure.dependencies import get_csv_dataframe_loader
from app.infrastructure.csv_dataframe_loader import CsvDataFrameLoader


class TestGetCsvDataFrameLoader:
    def test_returns_csv_dataframe_loader_instance(self):
        # Given / When
        result = get_csv_dataframe_loader()
        
        # Then
        assert isinstance(result, CsvDataFrameLoader)
