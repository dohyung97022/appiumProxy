from src.adb.domain.device import Device


class ProxyConnection:
    to_port: str
    device: Device

    def __init__(self,
                 to_port: str = None,
                 device: Device = None,
                 ):
        self.to_port = to_port
        self.device = device
