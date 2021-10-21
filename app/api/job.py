from fastapi import APIRouter, Depends
from core.config import GlobalSettings, get_settings
from service.jenkins import job
from model.schemas import jenkins as dto
from core.log import logger


router = APIRouter(
    prefix="/job",
    tags=["jenkins"],
    responses={404: {"description": "Not found"}},
)


@router.get("/jobs")
async def info(settings: GlobalSettings = Depends(get_settings)):
    joblists = job.getJobs(settings)

    return {
        "jobs": joblists,
        "length": len(joblists)
    }


# @router.get('/job/last_buildnumber')
# async def info(   settings: GlobalSettings = Depends(get_settings)):
#     joblists = job.getJobs(settings)

#     return {
#         "jobs": joblists,
#         "length": len(joblists)
#     }


@router.post('/trigger')
async def info(request_trigger_dto: dto.JenkinsTriggerDTO, settings: GlobalSettings = Depends(get_settings)):
    '''jenkins job trigger'''
    logger.info("----------------- jenkins job trigger API 호출 -----------------------")
    logger.info(f"요청정보 -> {request_trigger_dto.json()}")

    job.triggerJob(request_trigger_dto, settings)

    logger.info("----------------- jenkins job trigger API 호출 -----------------------")
    return {
        "done"
    }