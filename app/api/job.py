from fastapi import APIRouter, Depends
from core.config import GlobalSettings, get_settings
from service.jenkins.job import trigger as triggerservice
from service.jenkins.job import buildinfo as buildservice
from model.schemas import jenkins as dto
from core.log import logger
import json


router = APIRouter(
    prefix="/job",
    tags=["jenkins"],
    responses={404: {"description": "Not found"}},
)


# @router.get("/jobs")
# async def info(settings: GlobalSettings = Depends(get_settings)):
#     joblists = job.getJobs(settings)

#     return {
#         "jobs": joblists,
#         "length": len(joblists)
#     }


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
    logger.info(f"요청정보 -> {request_trigger_dto.jenkins_url}")

    build_id = triggerservice.triggerJob(request_trigger_dto, settings)

    logger.info("----------------- jenkins job trigger API 호출종료 -----------------------")

    return {
        "build_id": build_id
    }


@router.get('/build/log/{build_id}')
async def log(build_id: int, settings: GlobalSettings = Depends(get_settings)):
    '''jenkins log리턴'''
    logger.info("----------------- jenkins 빌드 log조회 API 호출 -----------------------")
    response = buildservice.getBuildLog(build_id, settings)

    logger.info("----------------- jenkins 빌드 log조회 API 호출종료 -----------------------")
    return response
