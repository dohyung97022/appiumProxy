import re
import time

from src.adb.domain.commands.device_state import DeviceState
from src.adb.domain.device import Device
from src.adb.domain.commands.adb_commands import AdbCommands
from src.dmesg.service import dmesg_service
from src.globals import global_params
from src.sub_process.service import subprocess_service


def get_all_devices() -> list[Device]:
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


def wifi_on(adb_key: str):
    process = subprocess_service.start(AdbCommands.wifi_on(adb_key))
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def wifi_off(adb_key: str):
    process = subprocess_service.start(AdbCommands.wifi_off(adb_key))
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def device_reconnect_tethering(device_key: str):
    print(f'reconnect device tethering : {device_key}')
    wifi_off(device_key)
    time.sleep(3)
    airplane_mode_off(device_key)
    time.sleep(3)
    lte_on(device_key)
    time.sleep(3)
    usb_tethering_on(device_key)


def device_reconnect_lte(device_key: str):
    print(f'reconnect device LTE : {device_key}')
    airplane_mode_on(device_key)
    time.sleep(3)
    airplane_mode_off(device_key)
    time.sleep(3)
    lte_on(device_key)
    time.sleep(3)


def check_connect_device_thread_job():
    devices = get_all_devices()
    key_to_device: dict[str, Device] = {}

    for adb_device in devices:
        # adb 의 권한이 지정되지 않은 경우
        if adb_device.state == DeviceState.UNAUTHORIZED:
            print(f'unauthorized device : {adb_device.key}, manual authorize is needed.')
            continue

        # global 내에 adb 로 조회한 key 가 존재하지 않을 경우
        device = global_params.key_to_device.get(adb_device.key, None)
        if device is None:
            device = adb_device

        # global 내에 port 가 존재하지 않을 경우
        port = global_params.key_to_port.get(adb_device.key, None)
        if port is None:
            global_params.key_to_port[adb_device.key] = global_params.get_available_port()

        # usb_connection 지정
        success, usb_connection = dmesg_service.get_device_usb_connection(device.key)
        if success:
            device.usb_connection = usb_connection

        # ethernet_key 지정
        success, ethernet_key = dmesg_service.get_usb_connection_ethernet_key(device.usb_connection)
        if success:
            device.ethernet_key = ethernet_key

        key_to_device[device.key] = device

    # adb 연결이 안된 key 제거
    global_params.key_to_device = key_to_device


def reconnect_device_thread_job():
    devices = global_params.key_to_device.values()
    for device in devices:
        if not device.is_valid_usb_tethering_connection():
            device_reconnect_tethering(device.key)
