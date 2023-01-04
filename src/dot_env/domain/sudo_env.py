from os import environ, getcwd
from dotenv import load_dotenv


# env 로드
load_dotenv(dotenv_path=getcwd() + '/src/dot_env/env/sudo.env')


# env 에서 받아온 db 정보
class SudoEnv:
    SUDO_PASSWORD = 'SUDO_PASSWORD'
    
    sudo_password = environ[SUDO_PASSWORD]
