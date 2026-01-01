import pytest
import pandas as pd
import io

from app.infrastructure.csv_dataframe_loader import CsvDataFrameLoader


class TestCsvDataFrameLoader:
    def test_load_valid_csv(self):
        # Given
        loader = CsvDataFrameLoader()
        csv_content = "name,age,city\nAlice,30,Tokyo\nBob,25,Osaka"
        csv_bytes = csv_content.encode('utf-8')
        
        # When
        result = loader.load(csv_bytes)
        
        # Then
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ["name", "age", "city"]
        assert result.iloc[0]["name"] == "Alice"
        assert result.iloc[0]["age"] == 30
        assert result.iloc[1]["name"] == "Bob"
        
    def test_load_empty_csv(self):
        # Given
        loader = CsvDataFrameLoader()
        csv_content = "col1,col2\n"
        csv_bytes = csv_content.encode('utf-8')
        
        # When
        result = loader.load(csv_bytes)
        
        # Then
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert list(result.columns) == ["col1", "col2"]
        
    def test_load_invalid_csv_raises_value_error(self):
        # Given
        loader = CsvDataFrameLoader()
        invalid_bytes = b"not a valid csv \x80\x81"
        
        # When / Then
        with pytest.raises(ValueError, match="Invalid CSV format"):
            loader.load(invalid_bytes)
