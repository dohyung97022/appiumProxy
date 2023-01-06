from subprocess import Popen

from src.adb.domain.device import Device
from src.proxy.domain.proxy_configuration import ProxyConfiguration


class GlobalParams:
    key_to_device: dict[str, Device] = {}

    proxy_server_process: Popen
    proxy_configuration: ProxyConfiguration = ProxyConfiguration()
    proxy_port_cnt: int = 3128


global_params = GlobalParams()
