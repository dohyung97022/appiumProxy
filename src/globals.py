from src.adb.domain.device import Device


class GlobalParams:
    key_to_device: dict[str, Device] = {}


global_params = GlobalParams()
