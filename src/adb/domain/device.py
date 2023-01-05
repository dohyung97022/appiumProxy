class Device:
    key: str
    state: str
    broadcast: str
    ipv4: str

    def __init__(self,
                 key: str = None,
                 state: str = None,
                 broadcast: str = None,
                 ipv4: str = None
                 ):
        self.key = key
        self.state = state
        self.broadcast = broadcast
        self.ipv4 = ipv4
