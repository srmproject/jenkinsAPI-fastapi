from core.config import GlobalSettings
from jenkinsapi.jenkins import Jenkins
from core.log import logger
from core.exceptions import jenkins
import requests
from requests.auth import HTTPBasicAuth
from model.schemas import jenkins as dto


def getJobs(settings: GlobalSettings):
    jenkins_host = settings.jenkins_host
    jenkins_user = settings.jenkins_user
    jenkins_password = settings.jenkins_password

    try:
        jenkins_client = Jenkins(
            jenkins_host,
            username=jenkins_user,
            password=jenkins_password
        )
        return [job[0] for job in jenkins_client.items()]

    except AssertionError as e:
        logger.error(f"job전체 조회API: jenkins 연결 실패 -> {e}")
        raise jenkins.FailConnection


# def getLastBuildNumber(settings: GlobalSettings):
#     '''Jenkins job빌드 마지막 번호 조회'''
#     try:
#         api_response = requests.post(
#             f"{settings.jenkins_host}?token={token}",
#             auth=HTTPBasicAuth(settings.jenkins_user, settings.jenkins_password)
#         )
#     except Exception as e:
#         logger.error(f"job 마지막빌드번호 조회: jenkins 연결 실패 -> {e}")
#         raise jenkins.FailConnection
#     else:
#         if not api_response.ok:
#             logger.error(f"job 마지막빌드번호 조회: jenkins 요청 실패 -> {api_response.content.decode('utf-8')}")
#             raise jenkins.FailRequest


def triggerJob(request_trigger_dto: dto.JenkinsTriggerDTO, settings: GlobalSettings):
    '''job트리거'''
    try:
        url = "{}{}/build?token={}".format(
            settings.jenkins_host,
            request_trigger_dto.jenkins_url,
            request_trigger_dto.token
        )
        logger.info(f"url -> {url}")
        api_response = requests.post(
            url,
            auth=HTTPBasicAuth(settings.jenkins_user, settings.jenkins_password)
        )
    except Exception as e:
        logger.error(f"job 트리거: jenkins 연결 실패 -> {e}")
        raise jenkins.FailConnection
    else:
        if not api_response.ok:
            logger.error(f"job 트리거: jenkins 요청 실패 -> {api_response.content.decode('utf-8')}")
            raise jenkins.FailRequest

        logger.info("job 트리거 성공")
        return getBuildhistoryNumber(api_response.headers)


def getBuildhistoryNumber(location):
    '''빌드 트리거된 item id파싱'''
    return int(location['Location'].split("item/")[1].replace("/", ""))
