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
