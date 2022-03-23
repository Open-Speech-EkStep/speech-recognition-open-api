import sys
import os

def set_root_folder_path():
    cwd = os.getcwd()
    sys.path.append(str(cwd))