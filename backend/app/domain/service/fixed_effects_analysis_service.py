from linearmodels.panel import PanelOLS
import pandas as pd

from app.domain.model.fixed_effects_result import FixedEffectsResult


class FixedEffectsAnalysisService:
    def __init__(
            self,
            dependent_var: str,
            independent_vars: list[str],
            entity_var: str,
            time_var: str,
    ):
        self.dependent_var = dependent_var
        self.independent_vars = independent_vars
        self.entity_var = entity_var
        self.time_var = time_var

    def analyze(self, dataframe: pd.DataFrame) -> FixedEffectsResult:
        df = dataframe.set_index([self.entity_var, self.time_var])

        y = df[self.dependent_var]
        x = df[self.independent_vars]

        fixed_effects_model = PanelOLS(y, x, entity_effects=True, drop_absorbed=True, check_rank=False)

        result = fixed_effects_model.fit()

        return FixedEffectsResult(
            nobs=int(result.nobs),
            params=result.params.to_dict(),
            std_errors=result.std_errors.to_dict(),
            tstats=result.tstats.to_dict(),
            pvalues=result.pvalues.to_dict(),
            rsquared_within=result.rsquared_within,
            rsquared_between=result.rsquared_between,
            rsquared_overall=result.rsquared_overall,
            dropped_vars=self._get_dropped_variables(result)
        )
        
    def _get_dropped_variables(self, result: FixedEffectsResult) -> list[str]:
        estimated_vars = set(result.params.index)
        original_vars = set(self.independent_vars)
        return sorted(original_vars - estimated_vars)
