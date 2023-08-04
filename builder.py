from cx_Freeze import setup, Executable
import sys
import os
import tutilities.basic as basic

current_dir = basic.get_directory(__file__)
dir_toBuild = f'{current_dir}toBuild{os.sep}'

# Update client.py (direct file edits) with updated connection values 
try:
        with open (f'') as f:
                for line in f:
                        if 'host = ' in str(line):
                                data = basic.fileRead(f'{dir_toBuild}client.py').replace(line, f"host = {build.get('host')}\n")
                                basic.fileWrite(f'{dir_toBuild}client.py',data)
                        if 'port = ' in str(line):
                                data = basic.fileRead(f'{dir_toBuild}client.py').replace(line, f"port = {build.get('port')}\n")
                                basic.fileWrite(f'{dir_toBuild}client.py',data)
                                
except Exception as e: print(e)

proj_name = "grayscale"
exe_name = "grayscale"
description = "Gangsters Real Edition"
                                
        

include_files = [f'{dir_toBuild}favicon.ico',]
base = None

#if sys.platform == "win32":
#    base = "Win32GUI"

def main():
        setup(name=proj_name,
        version="1.0",
        description=f"{description}",
        options={'build_exe': {'include_files': include_files}},
        executables=[Executable(
            f'{dir_toBuild}client.py',
            base=base,
            icon=f'{dir_toBuild}favicon.ico',
            target_name=f'{exe_name}.exe')])

if __name__ == '__main__':
    main()
