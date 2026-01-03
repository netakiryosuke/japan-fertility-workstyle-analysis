import pytest

from app.domain.model.fixed_effects_result import FixedEffectsResult


class TestFixedEffectsResult:
    def test_create_fixed_effects_result(self):
        # Given
        params = {"var1": 1.5, "var2": -0.3}
        std_errors = {"var1": 0.2, "var2": 0.1}
        tstats = {"var1": 7.5, "var2": -3.0}
        pvalues = {"var1": 0.001, "var2": 0.05}
        dropped_vars = []
        
        # When
        result = FixedEffectsResult(
            nobs=100,
            params=params,
            std_errors=std_errors,
            tstats=tstats,
            pvalues=pvalues,
            rsquared_within=0.75,
            rsquared_between=0.65,
            rsquared_overall=0.70,
            dropped_vars=dropped_vars
        )
        
        # Then
        assert result.nobs == 100
        assert result.params == params
        assert result.std_errors == std_errors
        assert result.tstats == tstats
        assert result.pvalues == pvalues
        assert result.rsquared_within == 0.75
        assert result.rsquared_between == 0.65
        assert result.rsquared_overall == 0.70
        assert result.dropped_vars == []
        
    def test_fixed_effects_result_is_immutable(self):
        # Given
        result = FixedEffectsResult(
            nobs=100,
            params={"var1": 1.5},
            std_errors={"var1": 0.2},
            tstats={"var1": 7.5},
            pvalues={"var1": 0.001},
            rsquared_within=0.75,
            rsquared_between=0.65,
            rsquared_overall=0.70,
            dropped_vars=[]
        )
        
        # When / Then
        import dataclasses
        with pytest.raises((AttributeError, dataclasses.FrozenInstanceError)):
            result.nobs = 200
