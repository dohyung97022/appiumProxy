class ProxyCommands:

    @classmethod
    def start_proxy(cls, configuration_file_location: str = "3proxy.cfg"):
        return ['3proxy', configuration_file_location]

    @classmethod
    def kill_all_proxy(cls):
        return ['killall', '3proxy']

    @classmethod
    def reboot_proxy_configuration(cls):
        return ['killall', '-s', 'USR1', '3proxy']
