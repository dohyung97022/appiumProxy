from src.proxy.domain.proxy_configuration import ProxyConfiguration


def create_configuration_file(proxy_configuration: ProxyConfiguration):
    proxy_configuration.create_configuration_file()
