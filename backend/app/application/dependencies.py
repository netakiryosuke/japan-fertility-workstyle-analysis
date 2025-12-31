from fastapi import Depends

from backend.app.application.fertility_analysis_application_service import FertilityAnalysisApplicationService
from backend.app.infrastructure.dependencies import get_csv_dataframe_loader

def get_fertility_analysis_application_service(
    csv_loader = Depends(get_csv_dataframe_loader),
) -> FertilityAnalysisApplicationService:
    return FertilityAnalysisApplicationService(csv_loader=csv_loader)
