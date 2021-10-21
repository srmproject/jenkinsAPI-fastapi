from pydantic import BaseModel

class JenkinsTriggerDTO(BaseModel):
    '''jenkins job트리거'''
    jenkins_url: str
    token: str
