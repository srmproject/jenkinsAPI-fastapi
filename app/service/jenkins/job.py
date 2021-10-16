

from app.core.config import Settings
from jenkinsapi.jenkins import Jenkins
from app.core.log import logger
from app.core.exceptions import jenkins


def getJobs(settgins: Settings):
    jenkins_host = settgins.jenkins_host
    jenkins_user = settgins.jenkins_user
    jenkins_password = settgins.jenkins_password

    try:
        jenkins_client = Jenkins(
            jenkins_host,
            username=jenkins_user,
            password=jenkins_password
        )
        return [job[0] for job in jenkins_client.items()]

    except AssertionError as e:
        logger.error("job전체 조회API-> jenkins 연결 실패")
        raise jenkins.FailConnection()
