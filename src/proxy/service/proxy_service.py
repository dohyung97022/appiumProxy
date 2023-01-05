from src.globals import global_params
from src.ifconfig.service import ifconfig_service
from src.proxy.domain.proxy_configuration import ProxyConfiguration


def create_configuration_file(proxy_configuration: ProxyConfiguration):
    proxy_configuration.create_configuration_file()


def check_connect_device_ipv4_thread_job():
    # 모든 interface_name 반환
    success, interface_names = ifconfig_service.get_all_interface_names()
    if not success:
        raise f"interface_names 를 읽을 수 없습니다."

    for interface_name in interface_names:

        # interface 반환
        success, ifconfig = ifconfig_service.get_ifconfig(interface_name)
        if not success:
            # 읽은 뒤에 바로 interface 가 사라진 경우
            continue

        # interface broadcast 반환
        _, broadcast = ifconfig_service.get_broadcast(ifconfig)

        # broadcast 와 일치하는 device 반환
        devices = global_params.key_to_device.values()
        devices = list(filter(lambda device: device.broadcast == broadcast, devices))
        device = devices[0] if len(devices) == 1 else None

        if device is not None:

            # 일치할 경우 ipv4 반환
            success, ipv4 = ifconfig_service.get_ipv4(ifconfig)
            if success:
                device.ipv4 = ipv4
                global_params.key_to_device[device.key] = device
                print(f'connected device {device.key}, {device.ipv4}')
