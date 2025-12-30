from backend.app.application.fertility_analysis_application_service import FertilityAnalysisApplicationService
from backend.app.domain.model.fixed_effects_result import FixedEffectsResult
from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter(prefix="/analysis", tags=["analysis"])

fertility_analysis_application_service = FertilityAnalysisApplicationService(csv_loader=None)


@router.post("", response_model=FixedEffectsResult)
async def analyze(
        csv_file: UploadFile = File(...),
        dependent_var: str = Form(...),
        independent_vars: list[str] = Form(...),
):
    csv_bytes = await csv_file.read()

    return fertility_analysis_application_service.analyze(
        csv_bytes,
        dependent_var,
        independent_vars
    )
