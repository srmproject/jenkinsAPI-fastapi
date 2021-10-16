from fastapi import APIRouter, Depends
from app.core.config import Settings, get_settings
from app.service.jenkins import job

router = APIRouter(
    prefix="/jenkins",
    tags=["jenkins"],
    responses={404: {"description": "Not found"}},
)


@router.get("/jobs")
async def info(settings: Settings = Depends(get_settings)):
    joblists = job.getJobs(settings)

    return {
        "jobs": joblists,
        "length": len(joblists)
    }
