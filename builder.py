from cx_Freeze import setup, Executable
import sys
import os
import tutilities.basic as basic

current_dir = basic.get_directory(__file__)
dir_toBuild = f'{current_dir}toBuild{os.sep}'

include_files = [f'{dir_toBuild}favicon.ico',]
base = None

#if sys.platform == "win32":
#    base = "Win32GUI"

def main():
        setup(name="grayscaleworkshop",
        version="1.0",
        description="grayscaleworkshop-client.exe",
        options={'build_exe': {'include_files': include_files}},
        executables=[Executable(
            f'{dir_toBuild}client.py',
            base=base,
            icon=f'{dir_toBuild}favicon.ico',
            target_name='grayscale-client.exe')])

if __name__ == '__main__':
    main()
