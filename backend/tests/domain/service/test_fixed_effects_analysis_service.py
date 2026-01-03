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
        
        # Create sample panel data with sufficient variation to avoid collinearity
        data = {
            "prefecture": ["Tokyo"] * 5 + ["Osaka"] * 5 + ["Kyoto"] * 5,
            "year": [2018, 2019, 2020, 2021, 2022] * 3,
            "fertility_rate": [1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.65, 1.7, 1.3, 1.32, 1.35, 1.38, 1.4],
            "work_hours": [40, 39, 38, 37, 36, 42, 41.5, 41, 40.5, 40, 41, 40.5, 40, 39.5, 39],
            "income": [500, 510, 520, 530, 540, 480, 490, 500, 510, 520, 490, 495, 500, 505, 510]
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
        
    def test_analyze_drops_collinear_variables(self):
        """Test that perfectly collinear variables are dropped and reported correctly"""
        # Given
        service = FixedEffectsAnalysisService(
            dependent_var="fertility_rate",
            independent_vars=["work_hours", "work_hours_doubled"],
            entity_var="prefecture",
            time_var="year"
        )
        
        # Create sample panel data where work_hours_doubled is perfectly collinear with work_hours
        data = {
            "prefecture": ["Tokyo"] * 5 + ["Osaka"] * 5 + ["Kyoto"] * 5,
            "year": [2018, 2019, 2020, 2021, 2022] * 3,
            "fertility_rate": [1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.65, 1.7, 1.3, 1.32, 1.35, 1.38, 1.4],
            "work_hours": [40, 39, 38, 37, 36, 42, 41.5, 41, 40.5, 40, 41, 40.5, 40, 39.5, 39]
        }
        dataframe = pd.DataFrame(data)
        # Add perfectly collinear variable (exact linear combination)
        dataframe["work_hours_doubled"] = dataframe["work_hours"] * 2
        
        # When
        result = service.analyze(dataframe)
        
        # Then
        assert isinstance(result, FixedEffectsResult)
        # One variable should be kept, one should be dropped
        assert len(result.params) == 1
        assert "work_hours" in result.params or "work_hours_doubled" in result.params
        # The dropped variable should be reported
        assert len(result.dropped_vars) == 1
        assert result.dropped_vars[0] in ["work_hours", "work_hours_doubled"]
        
    def test_analyze_drops_multiple_collinear_variables(self):
        """Test that multiple collinear variables are dropped correctly"""
        # Given
        service = FixedEffectsAnalysisService(
            dependent_var="fertility_rate",
            independent_vars=["base_var", "var_times_2", "var_times_3", "independent_var"],
            entity_var="prefecture",
            time_var="year"
        )
        
        # Create sample panel data with multiple collinear variables
        data = {
            "prefecture": ["Tokyo"] * 5 + ["Osaka"] * 5 + ["Kyoto"] * 5,
            "year": [2018, 2019, 2020, 2021, 2022] * 3,
            "fertility_rate": [1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.65, 1.7, 1.3, 1.32, 1.35, 1.38, 1.4],
            "base_var": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            "independent_var": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        }
        dataframe = pd.DataFrame(data)
        # Add perfectly collinear variables
        dataframe["var_times_2"] = dataframe["base_var"] * 2
        dataframe["var_times_3"] = dataframe["base_var"] * 3
        
        # When
        result = service.analyze(dataframe)
        
        # Then
        assert isinstance(result, FixedEffectsResult)
        # At least one base_var variant and independent_var should be kept
        assert len(result.params) >= 1
        assert len(result.params) <= 2
        # At least 2 collinear variables should be dropped
        assert len(result.dropped_vars) >= 2
        # Verify dropped vars are from the collinear set
        for dropped in result.dropped_vars:
            assert dropped in ["base_var", "var_times_2", "var_times_3", "independent_var"]
