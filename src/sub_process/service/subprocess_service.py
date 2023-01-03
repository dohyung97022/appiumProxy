import time
from subprocess import Popen, PIPE


# subprocess 시작
def start(cmd: list[str], cwd: str = '/') -> Popen:
    return Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=cwd)


def communicate(subprocess: Popen):
    return subprocess.communicate()


# subprocess 종료 여부를 반환
def is_finished(subprocess: Popen) -> bool:
    return subprocess.poll() is not None


# subprocess 끝날 때까지 대기
def wait_until_finished(subprocess: Popen, retry: int = 3600) -> bool:
    success = False
    for i in range(retry):
        time.sleep(1)
        success = is_finished(subprocess)
        if success:
            return success
    return success


# subprocess 종료
def kill(subprocess: Popen):
    subprocess.terminate()
    subprocess.kill()


# subprocess 모두 종료
def kill_all(subprocesses: list[Popen]):
    for subprocess in subprocesses:
        kill(subprocess)
