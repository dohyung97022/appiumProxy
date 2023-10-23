import os

from src.adb.service import adb_service
from src.globals import global_params
from src.proxy.domain.commands.proxy_commands import ProxyCommands
from src.proxy.domain.proxy_configuration import ProxyConfiguration
from src.proxy.domain.proxy_connection import ProxyConnection
from src.proxy.domain.proxy_user import ProxyUser
from src.sub_process.service import subprocess_service


def get_all_proxy_port() -> list:
    return list(global_params.key_to_port.values())


def kill_all_proxy():
    process = subprocess_service.start(ProxyCommands.kill_all_proxy(), sudo=True)
    subprocess_service.communicate(process, sudo=True)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def start_proxy():
    process = subprocess_service.start(ProxyCommands.start_proxy(), cwd=os.getcwd(), sudo=True)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def reboot_proxy_configuration():
    process = subprocess_service.start(ProxyCommands.reboot_proxy_configuration(), sudo=True)
    subprocess_service.communicate(process, sudo=True)
    subprocess_service.wait_until_finished(process)
    subprocess_service.kill(process)


def create_configuration_file(proxy_configuration: ProxyConfiguration):
    proxy_configuration.create_configuration_file()


def proxy_port_reconnect_ip(port: str) -> bool:
    success, device_key = global_params.get_device_key_of_port(int(port))
    if not success:
        raise '해당 포트에 할당된 device 가 없습니다.'

    adb_service.device_reconnect_lte(device_key)

    return True


def check_connect_device_into_3proxy_thread_job():
    devices = global_params.key_to_device.values()
    configuration = ProxyConfiguration(
        users=[ProxyUser(username='root', password='pass')],
    )

    for device in devices:
        if not device.is_valid_usb_tethering_connection():
            continue

        prev_connection = global_params.proxy_configuration.get_device_connection(device)

        connection = ProxyConnection()

        if prev_connection is not None:
            connection.to_port = prev_connection.to_port
        else:
            connection.to_port = global_params.key_to_port[device.key]

        connection.device = device

        # 연결이 유효할 경우에 config 추가
        configuration.connections.append(connection)

    for connection in configuration.connections:
        print(
            f'configuration device: {connection.device.key} interface:{connection.device.interface_name} ipv4:{connection.device.ipv4} ipv6:{connection.device.ipv6} to_port: {connection.to_port}')

    global_params.proxy_configuration = configuration

    global_params.proxy_configuration.create_configuration_file()

    reboot_proxy_configuration()
