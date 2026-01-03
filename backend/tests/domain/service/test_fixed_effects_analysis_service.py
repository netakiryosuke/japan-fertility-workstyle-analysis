import pytest
import pandas as pd

from app.domain.service.fixed_effects_analysis_service import FixedEffectsAnalysisService
from app.domain.model.fixed_effects_result import FixedEffectsResult


class TestFixedEffectsAnalysisService:
    def test_analyze_returns_fixed_effects_result(self):
        # Given
        service = FixedEffectsAnalysisService(
            dependent_var="fertility_rate",
            independent_vars=["work_hours", "income"],
            entity_var="prefecture",
            time_var="year"
        )
        
        # Create sample panel data
        data = {
            "prefecture": ["Tokyo", "Tokyo", "Tokyo", "Osaka", "Osaka", "Osaka"],
            "year": [2020, 2021, 2022, 2020, 2021, 2022],
            "fertility_rate": [1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
            "work_hours": [40, 38, 36, 42, 40, 38],
            "income": [500, 520, 540, 480, 500, 520]
        }
        dataframe = pd.DataFrame(data)
        
        # When
        result = service.analyze(dataframe)
        
        # Then
        assert isinstance(result, FixedEffectsResult)
        assert result.nobs > 0
        assert "work_hours" in result.params
        assert "income" in result.params
        assert isinstance(result.rsquared_within, float)
        assert isinstance(result.dropped_vars, list)
        
    def test_analyze_with_single_independent_variable(self):
        # Given
        service = FixedEffectsAnalysisService(
            dependent_var="fertility_rate",
            independent_vars=["work_hours"],
            entity_var="prefecture",
            time_var="year"
        )
        
        # Create more observations with variation to avoid collinearity
        data = {
            "prefecture": ["Tokyo"] * 5 + ["Osaka"] * 5 + ["Kyoto"] * 5,
            "year": [2018, 2019, 2020, 2021, 2022] * 3,
            "fertility_rate": [1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.65, 1.7, 1.3, 1.32, 1.35, 1.38, 1.4],
            "work_hours": [40, 39, 38, 37, 36, 42, 41.5, 41, 40.5, 40, 41, 40.5, 40, 39.5, 39]
        }
        dataframe = pd.DataFrame(data)
        
        # When
        result = service.analyze(dataframe)
        
        # Then
        assert isinstance(result, FixedEffectsResult)
        assert len(result.params) == 1
        assert "work_hours" in result.params
        assert isinstance(result.dropped_vars, list)
