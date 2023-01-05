import re
from src.ifconfig.domain.commands.ifconfig_commands import IfconfigCommands
from src.sub_process.service import subprocess_service


def get_ifconfig(interface_name: str) -> (bool, str):
    process = subprocess_service.start(IfconfigCommands.get_ifconfig_of_interface(interface_name))
    stdout, stderr = subprocess_service.communicate(process)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)

    if stderr != b'' or stdout is None:
        return False, None

    return True, stdout.decode('utf-8')


def get_all_interface_names() -> (bool, str):
    process = subprocess_service.start(IfconfigCommands.get_ifconfig())
    stdout, stderr = subprocess_service.communicate(process)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)

    if stderr != b'' or stdout is None:
        return False, None

    interface_names = re.findall(f'([^\s]*): flags=', stdout.decode('utf-8'))

    return True, interface_names


def get_ipv4(ifconfig: str) -> (bool, str):
    ipv4 = re.findall(f'inet ([^\s]*)  netmask', ifconfig)

    if len(ipv4) == 0:
        return False, None

    return True, ipv4[0]


def get_broadcast(ifconfig: str) -> (bool, str):
    bcast = re.findall(f'Bcast:([^\s]*)', ifconfig)
    broadcast = re.findall(f'broadcast ([^\s]*)', ifconfig)

    broadcast.extend(bcast)

    if len(broadcast) == 0:
        return False, None

    return True, broadcast[0]
