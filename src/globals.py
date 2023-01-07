from subprocess import Popen

from src.adb.domain.device import Device
from src.proxy.domain.proxy_configuration import ProxyConfiguration


class GlobalParams:
    key_to_device: dict[str, Device] = {}
    key_to_port: dict[str, int] = {}

    proxy_server_process: Popen
    proxy_configuration: ProxyConfiguration = ProxyConfiguration()
    proxy_port_cnt: int = 3128

    def get_device_key_of_port(self, port: int) -> (bool, str):
        for device_key, device_port in self.key_to_port.items():
            if device_port == port:
                return True, device_key

        return False, None


global_params = GlobalParams()
