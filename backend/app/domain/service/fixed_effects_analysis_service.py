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
        pass
