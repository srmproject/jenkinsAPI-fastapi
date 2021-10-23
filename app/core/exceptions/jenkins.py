class FailConnection(Exception):
    '''jenkins 연결실패'''
    def __init__(self):
        self.errors = "jenkins 연결실패"


class FailRequest(Exception):
    '''
    jenkins 요청실패
    (jenkins api연결은 되지만 요청이 실패한 경우)
    '''
    def __init__(self):
        self.errors = "jenkins 요청실패"


class NotExistBuildItem(Exception):
    '''
    jenkins buildhistory에 build_id가 미존재
    (실제 없거나 유효시간이 지난 build_id를 조회한 경우)
    '''
    def __init__(self, error_message):
        self.errors = "build로그 조회 실패"
        self.detail = error_message
        self.status_code = 404
