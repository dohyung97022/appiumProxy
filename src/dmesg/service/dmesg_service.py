import re

from src.dmesg.domain.commands.dmesg_commands import DmesgCommands
from src.sub_process.service import subprocess_service


def get_device_usb_connection(adb_key: str) -> (bool, str):
    process = subprocess_service.start(DmesgCommands.get_dmesg_device_usb_connection(adb_key), shell=True)
    stdout, stderr = subprocess_service.communicate(process)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)

    if stderr != b'' or stdout is None:
        return False, None

    usb_connections = re.findall(f'\[[0-9 ]+\.[0-9 ]+\] usb ([0-9-.]+)', stdout.decode('utf-8'))
    recent_usb_connection = usb_connections.pop()

    return True, recent_usb_connection


def get_usb_connection_ethernet_key(usb_connection: str) -> (bool, str):
    process = subprocess_service.start(DmesgCommands.get_usb_connection_ethernet_key(usb_connection), shell=True)
    stdout, stderr = subprocess_service.communicate(process)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)

    if stderr != b'' or stdout is None:
        return False, None

    ethernet_keys = re.findall(f'RNDIS device, ([0-9a-z:]+)', stdout.decode('utf-8'))
    recent_ethernet_key = ethernet_keys.pop()

    return True, recent_ethernet_key