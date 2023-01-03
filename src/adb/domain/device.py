class Device:
    key: str
    state: str

    def __init__(self, key: str, state: str):
        self.key = key
        self.state = state
