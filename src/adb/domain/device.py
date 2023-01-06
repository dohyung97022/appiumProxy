class Device:
    key: str
    state: str
    broadcast: str
    ipv4: str
    interface_name: str

    def __init__(self,
                 key: str = None,
                 state: str = None,
                 broadcast: str = None,
                 ipv4: str = None,
                 interface_name: str = None
                 ):
        self.key = key
        self.state = state
        self.broadcast = broadcast
        self.ipv4 = ipv4
        self.interface_name = interface_name

    def is_valid_usb_tethering_connection(self):
        return self.ipv4 is not None and \
               self.ipv4 != '127.0.0.1' and \
               self.broadcast is not None
