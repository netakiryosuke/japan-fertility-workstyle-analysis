from app.dependencies import get_dataframe_loader
from app.infrastructure.csv_dataframe_loader import CsvDataFrameLoader


class TestGetDataFrameLoader:
    def test_returns_csv_dataframe_loader_instance(self):
        # Given / When
        result = get_dataframe_loader()
        
        # Then
        assert isinstance(result, CsvDataFrameLoader)
