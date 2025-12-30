from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()

fertility_analysis_application_service = FertilityAnalysisApplicationService()


@router.post("/analysis")
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
