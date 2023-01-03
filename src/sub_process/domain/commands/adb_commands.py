class AdbCommands:

    @classmethod
    def get_all_devices(cls):
        return ['adb', 'devices']

    @classmethod
    def airplane_mode_on(cls, adb_key: str) -> list[str]:
        return ['adb', '-s', adb_key, 'shell', 'cmd', 'connectivity', 'airplane-mode', 'enable']

    @classmethod
    def airplane_mode_off(cls, adb_key: str) -> list[str]:
        return ['adb', '-s', adb_key, 'shell', 'cmd', 'connectivity', 'airplane-mode', 'disable']

    @classmethod
    def usb_tethering_on(cls, adb_key: str) -> list[str]:
        return ['adb', '-s', adb_key, 'shell', 'svc', 'usb', 'setFunctions', 'rndis']

    @classmethod
    def usb_tethering_off(cls, adb_key: str) -> list[str]:
        return ['adb', '-s', adb_key, 'shell', 'svc', 'usb', 'setFunctions']

    @classmethod
    def lte_on(cls, adb_key: str) -> list[str]:
        return ['adb', '-s', adb_key, 'shell', 'svc', 'data', 'enable']

    @classmethod
    def lte_off(cls, adb_key: str) -> list[str]:
        return ['adb', '-s', adb_key, 'shell', 'svc', 'data', 'disable']
