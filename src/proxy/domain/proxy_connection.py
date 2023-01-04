class ProxyConnection:
    to_port: str
    from_internal_ip: str

    def __init__(self,
                 to_port: str,
                 from_internal_ip: str
                 ):
        self.to_port = to_port
        self.from_internal_ip = from_internal_ip
