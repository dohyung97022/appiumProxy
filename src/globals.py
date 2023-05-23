from subprocess import Popen

from src.adb.domain.device import Device
from src.proxy.domain.proxy_configuration import ProxyConfiguration


class GlobalParams:
    key_to_device: dict[str, Device] = {}
    key_to_port: dict[str, int] = {}

    proxy_server_process: Popen
    proxy_configuration: ProxyConfiguration = ProxyConfiguration()
    proxy_port_start: int = 3128

    def get_device_key_of_port(self, port: int) -> (bool, str):
        for device_key, device_port in self.key_to_port.items():
            if device_port == port:
                return True, device_key

        return False, None

    def get_available_port(self):
        proxy_port = self.proxy_port_start

        while proxy_port in self.key_to_port.values():
            proxy_port = proxy_port + 1

        return proxy_port


global_params = GlobalParams()
