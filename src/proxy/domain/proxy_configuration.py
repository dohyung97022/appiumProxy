from src.adb.domain.device import Device
from src.proxy.domain.proxy_user import ProxyUser
from src.proxy.domain.proxy_auth import ProxyAuth
from src.proxy.domain.proxy_connection import ProxyConnection


class ProxyConfiguration:
    is_daemon: bool
    name_server: str
    name_server_cache: str
    users: list[ProxyUser]
    log_file: str
    log_rotation: int
    setgid: int
    setuid: int
    auth: ProxyAuth
    connections: list[ProxyConnection]
    is_flush: bool

    def __init__(self,
                 users: list[ProxyUser] = None,
                 connections: list[ProxyConnection] = None,
                 auth: ProxyAuth = ProxyAuth.NONE,
                 is_daemon: bool = True,
                 name_server: str = '8.8.8.8',
                 name_server_cache: str = '65536',
                 log_file: str = '/var/log/3proxy.log',
                 log_rotation: int = 30,
                 setgid: int = 13,
                 setuid: int = 13,
                 is_flush: bool = True,
                 ):
        if users is None:
            self.users = []
        else:
            self.users = users

        if connections is None:
            self.connections = []
        else:
            self.connections = connections

        self.auth = auth
        self.is_daemon = is_daemon
        self.name_server = name_server
        self.name_server_cache = name_server_cache
        self.log_file = log_file
        self.log_rotation = log_rotation
        self.setgid = setgid
        self.setuid = setuid
        self.is_flush = is_flush

    def get_device_connection(self, device: Device):
        for i in range(len(self.connections)):
            if self.connections[i].device.key == device.key:
                return self.connections[i]

        return None

    def create_configuration_file(self, configuration_file: str = "3proxy.cfg"):
        file = open(configuration_file, "w+")

        if self.is_daemon:
            file.write("daemon\n")

        file.write(f"nserver {self.name_server}\n")
        file.write(f"nscache {self.name_server_cache}\n")

        for user in self.users:
            file.write(f"users {user.username}:CL:{user.password}\n")

        file.write(f"log {self.log_file}\n")
        file.write(f"rotate {self.log_rotation}\n")
        file.write(f"setgid {self.setgid}\n")
        file.write(f"setuid {self.setuid}\n")
        file.write(f"auth {self.auth.value}\n")

        file.write("allow")
        for user in self.users:
            file.write(f" {user.username}")
        file.write("\n")

        for connection in self.connections:
            if connection.device.ipv4 is not None:
                file.write(f"proxy -p{connection.to_port} -e{connection.device.ipv4} -4 -De{connection.device.interface_name}\n")

            if connection.device.ipv6 is not None:
                file.write(f"proxy -p{connection.to_port} -e{connection.device.ipv6} -6 -De{connection.device.interface_name}\n")

        if self.is_flush:
            file.write("flush\n")
        file.close()
