import enum


class ProxyAuth(enum.Enum):
    STRONG = 'strong'
    NONE = 'none'
    IP_ONLY = 'iponly'
