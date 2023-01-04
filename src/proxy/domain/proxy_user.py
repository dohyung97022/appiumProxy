class ProxyUser:
    username: str
    password: str
    is_allowed: bool

    def __init__(self,
                 username: str,
                 password: str,
                 is_allowed: bool = True
                 ):
        self.username = username
        self.password = password
        self.is_allowed = is_allowed
