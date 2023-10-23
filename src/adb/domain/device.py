class Device:
    key: str
    state: str
    usb_connection: str
    ethernet_key: str
    ipv4: str
    ipv6: str
    interface_name: str

    def __init__(self,
                 key: str = None,
                 state: str = None,
                 usb_connection: str = None,
                 ethernet_key: str = None,
                 ipv4: str = None,
                 ipv6: str = None,
                 interface_name: str = None
                 ):
        self.key = key
        self.state = state
        self.usb_connection = usb_connection
        self.ethernet_key = ethernet_key
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.interface_name = interface_name

    def is_valid_usb_tethering_connection(self):
        return self.ipv4 is not None and \
               self.ipv4 != '127.0.0.1' and \
               self.ethernet_key is not None
