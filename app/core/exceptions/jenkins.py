class FailConnection(Exception):
    '''jenkins 연결실패'''
    def __init__(self):
        self.errors = "jenkins 연결실패"
