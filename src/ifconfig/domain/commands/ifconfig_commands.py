class IfconfigCommands:

    @classmethod
    def get_ifconfig(cls):
        return ['ifconfig']

    @classmethod
    def get_ifconfig_of_interface(cls, interface: str):
        return ['ifconfig', interface]
