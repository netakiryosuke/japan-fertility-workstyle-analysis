from app.application.exception.missing_columns_exception import MissingColumnsException


class TestMissingColumnsException:
    def test_exception_with_single_missing_column(self):
        # Given
        missing_columns = ["column1"]
        
        # When
        exception = MissingColumnsException(missing_columns)
        
        # Then
        assert exception.missing_columns == missing_columns
        assert "column1" in str(exception)
        assert "Required columns are missing" in str(exception)
        
    def test_exception_with_multiple_missing_columns(self):
        # Given
        missing_columns = ["column1", "column2", "column3"]
        
        # When
        exception = MissingColumnsException(missing_columns)
        
        # Then
        assert exception.missing_columns == missing_columns
        assert "column1" in str(exception)
        assert "column2" in str(exception)
        assert "column3" in str(exception)
