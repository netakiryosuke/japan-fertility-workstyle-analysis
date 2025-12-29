from backend.app.domain.model.fixed_effects_result import FixedEffectsResult
from backend.app.domain.service.fixed_effects_analysis_service import FixedEffectsAnalysisService
from backend.app.infrastructure.csv_dataframe_loader import CsvDataFrameLoader


class FertilityAnalysisApplicationService:
    def __init__(self):
        self.csv_loader = CsvDataFrameLoader()

    def analyze(
        self,
        csv_bytes: bytes,
        dependent_var: str,
        independent_vars: list[str],
        entity_var: str = "prefecture",
        time_var: str = "year"
    ) -> FixedEffectsResult:

        dataframe = self.csv_loader.load(csv_bytes)

        analysis_service = FixedEffectsAnalysisService(
            dependent_var=dependent_var,
            independent_vars=independent_vars,
            entity_var=entity_var,
            time_var=time_var
        )

        return analysis_service.analyze(dataframe)
