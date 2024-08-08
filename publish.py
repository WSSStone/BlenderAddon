import os
import configparser
import subprocess

config = configparser.ConfigParser()
config.read('config.ini')
WINRAR = config['Paths']['winrar_path']
SRC_DIR = os.path.realpath("./src")
DST_DIR = os.path.realpath("./out")

def zip(addon:str):
    cwd = os.getcwd()

    src = os.path.join(SRC_DIR, addon)
    dst = os.path.join(DST_DIR, addon)

    os.chdir(src)

    cmd = f'"{WINRAR}" a -r -afzip "{dst}.zip" "*"'

    subprocess.run(cmd, shell=True, cwd=os.getcwd())

    os.chdir(cwd)

def publish():    
    for addon in os.listdir(SRC_DIR):
        zip(addon)
    
def cleanup():
    for f in os.listdir(DST_DIR):
        os.remove(os.path.join(DST_DIR, f))

def check():
    if not os.path.exists(f'{WINRAR}'):
        print(f'{WINRAR}')
        raise Exception("WinRAR not found. Configure WinRAR path in config.ini.")

    if not os.path.exists(SRC_DIR):
        raise Exception("Source directory lost. Repull repo.")
    
    os.makedirs(DST_DIR, exist_ok=True)

def main():
    check()

    cleanup()

    publish()

    print("===== FINISHED =====")

if __name__ == '__main__':
    main()