from src.utils.module import module_utils

controller_ends_with = 'controller.py'


def configure():
    controller_config()


# 모든 controller import
def controller_config():
    module_utils.import_all_modules_ends_with(controller_ends_with)
