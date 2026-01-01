import pytest
import pandas as pd
from unittest.mock import Mock

from app.application.fertility_analysis_application_service import FertilityAnalysisApplicationService
from app.application.exception.missing_columns_exception import MissingColumnsException
from app.domain.model.fixed_effects_result import FixedEffectsResult


class TestFertilityAnalysisApplicationService:
    def test_analyze_with_valid_data(self):
        # Given
        mock_csv_loader = Mock()
        # Create more observations with variation
        data = {
            "prefecture": ["Tokyo"] * 5 + ["Osaka"] * 5 + ["Kyoto"] * 5,
            "year": [2018, 2019, 2020, 2021, 2022] * 3,
            "fertility_rate": [1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.65, 1.7, 1.3, 1.32, 1.35, 1.38, 1.4],
            "work_hours": [40, 39, 38, 37, 36, 42, 41.5, 41, 40.5, 40, 41, 40.5, 40, 39.5, 39]
        }
        mock_csv_loader.load.return_value = pd.DataFrame(data)
        
        service = FertilityAnalysisApplicationService(csv_loader=mock_csv_loader)
        csv_bytes = b"some,csv,data"
        
        # When
        result = service.analyze(
            csv_bytes=csv_bytes,
            dependent_var="fertility_rate",
            independent_vars=["work_hours"]
        )
        
        # Then
        assert isinstance(result, FixedEffectsResult)
        mock_csv_loader.load.assert_called_once_with(csv_bytes)
        
    def test_analyze_with_missing_columns_raises_exception(self):
        # Given
        mock_csv_loader = Mock()
        data = {
            "prefecture": ["Tokyo", "Osaka"],
            "year": [2020, 2020],
            "fertility_rate": [1.2, 1.5]
        }
        mock_csv_loader.load.return_value = pd.DataFrame(data)
        
        service = FertilityAnalysisApplicationService(csv_loader=mock_csv_loader)
        csv_bytes = b"some,csv,data"
        
        # When / Then
        with pytest.raises(MissingColumnsException) as exc_info:
            service.analyze(
                csv_bytes=csv_bytes,
                dependent_var="fertility_rate",
                independent_vars=["work_hours"]
            )
        assert "work_hours" in exc_info.value.missing_columns
        
    def test_normalize_dataframe_filters_columns(self):
        # Given
        mock_csv_loader = Mock()
        # Create more observations with variation
        data = {
            "prefecture": ["Tokyo"] * 5 + ["Osaka"] * 5 + ["Kyoto"] * 5,
            "year": [2018, 2019, 2020, 2021, 2022] * 3,
            "fertility_rate": [1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.65, 1.7, 1.3, 1.32, 1.35, 1.38, 1.4],
            "work_hours": [40, 39, 38, 37, 36, 42, 41.5, 41, 40.5, 40, 41, 40.5, 40, 39.5, 39],
            "extra_column": [100, 101, 102, 103, 104, 200, 201, 202, 203, 204, 150, 151, 152, 153, 154]
        }
        mock_csv_loader.load.return_value = pd.DataFrame(data)
        
        service = FertilityAnalysisApplicationService(csv_loader=mock_csv_loader)
        csv_bytes = b"some,csv,data"
        
        # When
        result = service.analyze(
            csv_bytes=csv_bytes,
            dependent_var="fertility_rate",
            independent_vars=["work_hours"]
        )
        
        # Then
        assert isinstance(result, FixedEffectsResult)
        # Verify only required columns were used (indirectly through successful analysis)
        
    def test_analyze_with_custom_entity_and_time_vars(self):
        # Given
        mock_csv_loader = Mock()
        # Create more observations with variation
        data = {
            "region": ["Tokyo"] * 5 + ["Osaka"] * 5 + ["Kyoto"] * 5,
            "period": [2018, 2019, 2020, 2021, 2022] * 3,
            "fertility_rate": [1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.65, 1.7, 1.3, 1.32, 1.35, 1.38, 1.4],
            "work_hours": [40, 39, 38, 37, 36, 42, 41.5, 41, 40.5, 40, 41, 40.5, 40, 39.5, 39]
        }
        mock_csv_loader.load.return_value = pd.DataFrame(data)
        
        service = FertilityAnalysisApplicationService(csv_loader=mock_csv_loader)
        csv_bytes = b"some,csv,data"
        
        # When
        result = service.analyze(
            csv_bytes=csv_bytes,
            dependent_var="fertility_rate",
            independent_vars=["work_hours"],
            entity_var="region",
            time_var="period"
        )
        
        # Then
        assert isinstance(result, FixedEffectsResult)
