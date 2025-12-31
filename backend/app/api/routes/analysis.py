from fastapi import APIRouter, UploadFile, File, Form, Depends

from app.application.fertility_analysis_application_service import FertilityAnalysisApplicationService
from app.domain.model.fixed_effects_result import FixedEffectsResult
from app.application.dependencies import get_fertility_analysis_application_service

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("", response_model=FixedEffectsResult)
async def analyze(
        csv_file: UploadFile = File(...),
        dependent_var: str = Form(...),
        independent_vars: list[str] = Form(...),
        fertility_analysis_application_service: FertilityAnalysisApplicationService = Depends(get_fertility_analysis_application_service)
) -> FixedEffectsResult:
    csv_bytes = await csv_file.read()

    return fertility_analysis_application_service.analyze(
        csv_bytes,
        dependent_var,
        independent_vars
    )
