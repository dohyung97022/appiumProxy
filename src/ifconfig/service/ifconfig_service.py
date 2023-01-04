import re

from src.ifconfig.domain.commands.ifconfig_commands import IfconfigCommands
from src.ifconfig.domain.ifconfig_interface import IfconfigInterface
from src.sub_process.service import subprocess_service


def get_ifconfig_interface(interface_name: str) -> (bool, IfconfigInterface):
    process = subprocess_service.start(IfconfigCommands.get_ifconfig(interface_name))
    stdout, stderr = subprocess_service.communicate(process)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)

    if stderr != b'':
        return False, None

    msg = stdout.decode('utf-8')

    ipv4 = re.findall(f'inet ([^\s]*)  netmask', msg)

    if len(ipv4) == 0:
        return False, None

    ipv4 = ipv4[0]

    ifconfig_interface = IfconfigInterface(
        internal_ipv4=ipv4
    )

    return True, ifconfig_interface
