class DmesgCommands:

    @classmethod
    def get_dmesg_device_usb_connection(cls, adb_key: str):
        return ['dmesg', '|', 'grep', f"'SerialNumber: {adb_key}'"]

    @classmethod
    def get_usb_connection_ethernet_key(cls, usb_connection: str):
        return ['dmesg', '|', 'grep', f"'rndis_host {usb_connection}'"]
