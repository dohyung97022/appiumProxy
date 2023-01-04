import re

from src.dmesg.domain.commands.dmesg_commands import DmesgCommands
from src.sub_process.service import subprocess_service


def get_dmesg() -> (bool, str):
    process = subprocess_service.start(DmesgCommands.get_dmesg(), sudo=True)
    stdout, stderr = subprocess_service.communicate(process, sudo=True)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)

    if stderr != b'':
        return False, None

    return True, stdout.decode("utf-8")


def get_usb_code_by_device_key(dmesg: str, device_key: str) -> (bool, str):
    found = re.findall(f'usb ([^\s]*): SerialNumber: {device_key}', dmesg)

    if len(found) == 0:
        return False, None

    return True, found[len(found) - 1]


def get_interface_name_by_usb_code(dmesg: str, usb_code: str) -> (bool, str):
    found = re.findall(f'rndis_host {usb_code}:[^\s]* ([^\s]*):', dmesg)

    if len(found) == 0:
        return False, None

    return True, found[len(found) - 1]
