import re
import time

from src.adb.domain.device import Device
from src.adb.domain.commands.adb_commands import AdbCommands
from src.globals import global_params
from src.ifconfig.service import ifconfig_service
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


def get_device_ifconfig(adb_key: str, interface_name: str = 'rndis0') -> (bool, str):
    process = subprocess_service.start(AdbCommands.get_device_ifconfig(adb_key, interface_name))
    stdout, stderr = subprocess_service.communicate(process)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)

    if stderr != b'' or stdout is None:
        return False, None

    return True, stdout.decode('utf-8')


def reconnect_usb_tethering(device: Device):
    print(f'reconnecting device : {device.key}')
    airplane_mode_off(device.key)
    time.sleep(3)
    lte_on(device.key)
    time.sleep(3)
    usb_tethering_off(device.key)
    time.sleep(3)
    usb_tethering_on(device.key)


def check_connect_device_thread_job():
    devices = get_all_devices()

    for adb_device in devices:
        # global_params 안에 있을 경우
        device = global_params.key_to_device.get(adb_device.key, None)
        if device is None:
            # global_params 안에 저장되지 않을 경우
            global_params.key_to_device[adb_device.key] = adb_device
            device = adb_device

        # 기기의 테더링 ifconfig 반환
        success, device_ifconfig = get_device_ifconfig(device.key, interface_name='rndis0')
        if not success:
            device.broadcast = None
            global_params.key_to_device[device.key] = device
            continue

        # 기기의 테더링 broadcast 반환
        success, device_broadcast = ifconfig_service.get_broadcast(device_ifconfig)
        if not success:
            raise f"broadcast 를 읽을 수 없습니다. device_ifconfig: {device_ifconfig}"

        device.broadcast = device_broadcast
        global_params.key_to_device[device.key] = device


def reconnect_device_thread_job():
    devices = global_params.key_to_device.values()
    for device in devices:
        print(f'checking device key : {device.key} ipv4 : {device.ipv4} broadcast : {device.broadcast}')
        if device.ipv4 is None or device.ipv4 is '127.0.0.1' or device.broadcast is None:
            reconnect_usb_tethering(device)
