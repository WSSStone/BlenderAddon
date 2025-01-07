import os
import configparser
import subprocess
import git

class addon_publisher:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.WINRAR = self.config['Paths']['winrar_path']
        self.SRC_DIR = os.path.realpath("./src")
        self.DST_DIR = os.path.realpath("./out")
        
        self.changed_addons = {}

    def zip(self, addon:str):
        cwd = os.getcwd()

        src = os.path.join(self.SRC_DIR, addon)
        dst = os.path.join(self.DST_DIR, addon)

        os.chdir(src)

        cmd = f'"{self.WINRAR}" a -r -afzip "{dst}.zip" "*"'

        subprocess.run(cmd, shell=True, cwd=os.getcwd())

        os.chdir(cwd)

    def publish(self):    
        for addon in self.changed_addons:
            self.zip(addon)
        
    def cleanup(self):
        for addon in self.changed_addons:
            p = os.path.join(self.DST_DIR, f'{addon}.zip')
            if os.path.exists(p):
                os.remove(p)

    def check_changes(self):
        repo = git.Repo(os.getcwd())

        diff = repo.index.diff(None)
        for item in diff:
            if 'src/' in item.a_path:
                addon = item.a_path.split('/')[1]
                self.changed_addons[addon] = True

    def check_dependency(self):
        if not os.path.exists(f'{self.WINRAR}'):
            print(f'{self.WINRAR}')
            raise Exception("WinRAR not found. Configure WinRAR path in config.ini.")

        if not os.path.exists(self.SRC_DIR):
            raise Exception("Source directory lost. Repull repo.")
        
        os.makedirs(self.DST_DIR, exist_ok=True)

    def main(self):
        self.check_dependency()

        self.check_changes()

        self.cleanup()

        self.publish()

        print("===== FINISHED =====")

if __name__ == '__main__':
    publisher = addon_publisher()
    publisher.main()