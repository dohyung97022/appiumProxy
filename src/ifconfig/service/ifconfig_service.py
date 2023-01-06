import re
from src.globals import global_params
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


def get_interface_name(ifconfig: str) -> (bool, str):
    interface_names = re.findall(f'([^\s]*): flags=', ifconfig)

    if len(interface_names) == 0:
        return False, None

    return True, interface_names[0]


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


def check_connect_device_ipv4_thread_job():
    # 모든 interface_name 반환
    success, interface_names = get_all_interface_names()
    if not success:
        raise f"interface_names 를 읽을 수 없습니다."

    for interface_name in interface_names:

        # interface 반환
        success, ifconfig = get_ifconfig(interface_name)
        if not success:
            # 읽은 뒤에 바로 interface 가 사라진 경우
            continue

        # broadcast, name 반환
        _, broadcast = get_broadcast(ifconfig)
        _, interface_name = get_interface_name(ifconfig)

        # broadcast 와 일치하는 device 반환
        devices = global_params.key_to_device.values()
        devices = list(filter(lambda device: device.broadcast == broadcast, devices))
        device = devices[0] if len(devices) == 1 else None

        if device is not None:

            # 일치할 경우 ipv4 반환
            success, ipv4 = get_ipv4(ifconfig)
            if success:
                device.ipv4 = ipv4
                device.interface_name = interface_name
