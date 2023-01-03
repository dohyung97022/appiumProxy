import importlib
import os
from types import ModuleType


# 해당 문구로 끝나는 module import
def import_all_modules_ends_with(ends_with: str) -> list[ModuleType]:
    modules: list[ModuleType] = []
    for root, dirs, files in os.walk('./src'):
        for file in files:
            if file.endswith(ends_with):
                # get path
                location_path = os.path.join(root, file)
                # reformat
                import_path = location_path_to_import_path(location_path)
                # import
                modules.append(importlib.import_module(import_path))

    return modules


# 파일 위치 명을 import 명으로 변경
def location_path_to_import_path(location_path: str) -> str:
    location_path = location_path.replace('./', '', 1)
    location_path = location_path.replace('/', '.')
    location_path = location_path.replace('.py', '', 1)
    return location_path
