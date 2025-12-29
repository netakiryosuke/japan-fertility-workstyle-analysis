from linearmodels.panel import PanelOLS

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

    def analyze(self, dataframe) -> dict:
        df = dataframe.set_index([self.entity_var, self.time_var])

        y = df[self.dependent_var]
        x = df[self.independent_vars]

        fixed_effects_model = PanelOLS(y, x, entity_effects=True)

        result = fixed_effects_model.fit()

        return {
            "nobs": int(result.nobs),
            "params": result.params.to_dict(),
            "std_errors": result.std_errors.to_dict(),
            "tstats": result.tstats.to_dict(),
            "pvalues": result.pvalues.to_dict(),
            "rsquared": {
                "within": result.rsquared_within,
                "between": result.rsquared_between,
                "overall": result.rsquared_overall,
            }
        }
