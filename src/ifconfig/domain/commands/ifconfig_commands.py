class IfconfigCommands:

    @classmethod
    def get_ifconfig(cls, interface: str):
        return ['ifconfig', interface]
