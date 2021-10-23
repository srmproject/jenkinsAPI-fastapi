from pydantic import BaseModel

class JenkinsTriggerDTO(BaseModel):
    '''jenkins job트리거'''
    jenkins_url: str
    token: str


class ResponseBuildLogDTO(BaseModel):
    '''jenkins 빌드로그조회 응답'''
    result: str
    size: int
    stages: list
