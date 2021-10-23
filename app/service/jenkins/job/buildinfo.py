import requests
from core.config import GlobalSettings
from core.log import logger
from core.exceptions import jenkins as exception
from requests.auth import HTTPBasicAuth
import json
from model.schemas import jenkins as jenkins_schemas


def getBuildInfoInHistory(build_id: int, settings: GlobalSettings):
    '''빌드 item 조회'''
    try:
        url = "{}/queue/item/{}/api/json".format(
            settings.jenkins_host,
            build_id
        )
        api_response = requests.get(
            url,
            auth=HTTPBasicAuth(settings.jenkins_user, settings.jenkins_password)
        )
    except Exception as e:
        logger.error(f"job builditem조회: jenkins 연결 실패 -> {e}")
        raise exception.FailConnection
    else:
        if not api_response.ok:
            if api_response.status_code == 404:
                logger.error(f"job builditem조회: jenkins 요청 실패 -> 빌드 히스토리에 {build_id}가 없습니다.")
                raise exception.NotExistBuildItem(f"빌드 히스토리에 {build_id}가 없습니다.")
            else:
                logger.error(f"job builditem조회: jenkins 연결 실패 -> {api_response.content.decode('utf-8')}")
                raise exception.FailRequest

        logger.info("job builditem조회 성공")
        return api_response.json()


def getBuildDetail(build_detail_url, settings: GlobalSettings):
    '''build정보 조회'''
    try:
        url = f"{build_detail_url}api/json"
        logger.debug(f"build_detail_url: {url}")
        api_response = requests.get(
            url,
            auth=HTTPBasicAuth(settings.jenkins_user, settings.jenkins_password)
        )
    except Exception as e:
        logger.error(f"job build정보조회: jenkins 연결 실패 -> {e}")
        raise exception.FailConnection
    else:
        if not api_response.ok:
            if api_response.status_code == 404:
                logger.error(f"build정보조회: jenkins 요청 실패 -> 빌드중이지 않습니다.")
                raise exception.NotExistBuildItem(f"빌드중이지 않습니다.")
            else:
                logger.error(f"build정보조회: jenkins 연결 실패 -> {api_response.content.decode('utf-8')}")
                raise exception.FailRequest

        logger.info("job build정보조회 성공")
        return json.dumps(api_response.json())


def isReady(build_info):
    '''
    빌드준비중인지 확인
    :return
        True: 준비 중
        False: 준비 완료
    '''
    if build_info.get('why'):
        # return "In the quiet period" in build_info.get('why')
        return True

    return False


def getWorkflow(job_name:str, build_number:int, settings: GlobalSettings):
    '''
    job workflow 조회
    :return list
    '''
    log_prefix = "job build worflow 조회"

    try:
        url = f"{job_name}wfapi/runs"
        api_response = requests.get(
            url,
            auth=HTTPBasicAuth(settings.jenkins_user, settings.jenkins_password)
        )
    except Exception as e:
        logger.error(f"{log_prefix}: jenkins 연결 실패 -> {e}")
        raise exception.FailConnection
    else:
        if not api_response.ok:
            if api_response.status_code == 404:
                logger.error(f"{log_prefix}: jenkins 요청 실패 -> 빌드중이지 않습니다.")
                raise exception.NotExistBuildItem(f"빌드중이지 않습니다.")
            else:
                logger.error(f"{log_prefix}: jenkins 연결 실패 -> {api_response.content.decode('utf-8')}")
                raise exception.FailRequest

        logger.info(f"{log_prefix} 성공")
        return api_response.json()


def getCurrentWorkflow(workflows, build_number):
    '''현재 빌드중인 workflow조회'''

    for workflow in workflows:
        if int(workflow['id']) == build_number:
            return workflow

    return False


def getBuildLog(build_id: int, settings: GlobalSettings):
    build_info = getBuildInfoInHistory(build_id, settings)

    if isReady(build_info):
        return {"status": "준비 중"}

    build_number = build_info['executable']['number']
    job_name = build_info['executable']['url'].split(str(build_number)+"/")[0]

    worfklows = getWorkflow(job_name, build_number, settings)
    current_workflow = getCurrentWorkflow(worfklows, build_number)

    if not current_workflow:
        logger.error(f"빌드로그 조회: {build_id}는 빌드중이지 않습니다.")
        raise exception.NotExistBuildItem(f"{build_id}는 빌드중이지 않습니다.")

    stages = []
    for stage in current_workflow['stages']:
        stages.append({
            "name": stage["name"],
            "detail_url": stage["_links"]["self"]["href"],
            "status": stage["status"],
            "startTimeMillis": stage["startTimeMillis"],
            "durationMillis": stage["durationMillis"]
        })

    return jenkins_schemas.ResponseBuildLogDTO(
        result=current_workflow['status'],
        size=len(stages),
        stages=stages,

    )
