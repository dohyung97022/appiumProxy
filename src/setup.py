from src.adb.service.adb_service import check_connect_device_thread_job, reconnect_device_thread_job
from src.ifconfig.service.ifconfig_service import check_connect_device_ipv4_thread_job
from src.utils.module import module_utils
from src.utils.thread.thread_utils import BatchJob

controller_ends_with = 'controller.py'


def configure():
    controller_config()
    thread_config()


# 모든 controller import
def controller_config():
    module_utils.import_all_modules_ends_with(controller_ends_with)


def thread_config():
    batch_job = BatchJob(method=check_connect_device_thread_job, interval=1)
    batch_job.start()

    batch_job = BatchJob(method=check_connect_device_ipv4_thread_job, interval=1)
    batch_job.start()

    batch_job = BatchJob(method=reconnect_device_thread_job, interval=20)
    batch_job.start()
