from fastapi import Depends

from app.application.fertility_analysis_application_service import FertilityAnalysisApplicationService
from app.infrastructure.dependencies import CsvDataFrameLoader, get_csv_dataframe_loader

def get_fertility_analysis_application_service(
    csv_loader: CsvDataFrameLoader = Depends(get_csv_dataframe_loader),
) -> FertilityAnalysisApplicationService:
    return FertilityAnalysisApplicationService(csv_loader=csv_loader)
