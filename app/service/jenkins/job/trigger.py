from core.config import GlobalSettings
from core.log import logger
from core.exceptions import jenkins as exception
import requests
from requests.auth import HTTPBasicAuth
from model.schemas import jenkins as dto


def triggerJob(request_trigger_dto: dto.JenkinsTriggerDTO, settings: GlobalSettings):
    '''job트리거'''
    try:
        url = "{}{}/build?token={}".format(
            settings.jenkins_host,
            request_trigger_dto.jenkins_url,
            request_trigger_dto.token
        )
        api_response = requests.post(
            url,
            auth=HTTPBasicAuth(settings.jenkins_user, settings.jenkins_password)
        )
    except Exception as e:
        logger.error(f"job 트리거: jenkins 연결 실패 -> {e}")
        raise exception.FailConnection
    else:
        if not api_response.ok:
            logger.error(f"job 트리거: jenkins 요청 실패 -> {api_response.content.decode('utf-8')}")
            raise exception.FailRequest

        logger.info("job 트리거 성공")
        return getBuildhistoryNumber(api_response.headers)


def getBuildhistoryNumber(location):
    '''빌드 트리거된 item id파싱'''
    return int(location['Location'].split("item/")[1].replace("/", ""))
