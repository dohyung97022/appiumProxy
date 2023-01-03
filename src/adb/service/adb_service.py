import re

from src.adb.domain.device import Device
from src.sub_process.domain.commands.adb_commands import AdbCommands
from src.sub_process.service import subprocess_service


def get_all_devices():
    process = subprocess_service.start(AdbCommands.get_all_devices())
    stdout, stderr = subprocess_service.communicate(process)
    output = stdout.decode('utf8')
    subprocess_service.kill(process)
    adb_keys = re.findall('\n([^\s]*)\t', output)
    adb_states = re.findall('\n[^\s]*\t([^\s]*)', output)

    devices: list[Device] = []
    for i in range(len(adb_keys)):
        devices.append(Device(key=adb_keys[i], state=adb_states[i]))

    return devices


def airplane_mode_on(adb_key: str):
    process = subprocess_service.start(AdbCommands.airplane_mode_on(adb_key))
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def airplane_mode_off(adb_key: str):
    process = subprocess_service.start(AdbCommands.airplane_mode_off(adb_key))
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def usb_tethering_on(adb_key: str):
    process = subprocess_service.start(AdbCommands.usb_tethering_on(adb_key))
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def usb_tethering_off(adb_key: str):
    process = subprocess_service.start(AdbCommands.usb_tethering_off(adb_key))
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def lte_on(adb_key: str):
    process = subprocess_service.start(AdbCommands.lte_on(adb_key))
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def lte_off(adb_key: str):
    process = subprocess_service.start(AdbCommands.lte_off(adb_key))
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)
