
from fastapi import Depends

from app.infrastructure.csv_dataframe_loader import CsvDataFrameLoader
from app.domain.dataframe_loader import DataFrameLoader
from app.application.fertility_analysis_application_service import FertilityAnalysisApplicationService

def get_dataframe_loader() -> DataFrameLoader:
    return CsvDataFrameLoader()

def get_fertility_analysis_application_service(
    csv_loader: CsvDataFrameLoader = Depends(get_dataframe_loader),
) -> FertilityAnalysisApplicationService:
    return FertilityAnalysisApplicationService(csv_loader=csv_loader)
