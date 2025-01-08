import os
import sys
import configparser
import subprocess
import git

class extension_publisher:
    def __init__(self):
        self.config = configparser.ConfigParser()

        self.config.read('config.ini')

        self.BLENDER = self.config['Paths']['blender_path']

        self.SRC_DIR = self.config['Paths']['src_dir']

        self.DST_DIR = self.config['Paths']['dst_dir']

        self.publications = {}


    def build(self, ext:str):
        cwd = os.getcwd()

        src = os.path.join(self.SRC_DIR, ext)

        dst = os.path.join(self.DST_DIR, ext)

        os.chdir(src)

        cmd = f'{self.BLENDER} --command extension build --split-platforms --output-dir {self.DST_DIR}'

        p = subprocess.Popen(cmd, shell=True, cwd=os.getcwd())

        p.wait()

        os.chdir(cwd)


    def publish(self):    
        for ext in self.publications:
            self.build(ext)            

    def cleanup(self):
        for ext in self.publications:
            p = os.path.join(self.DST_DIR, f'{ext}-1.0.0-windows_x64.zip')

            if os.path.exists(p):
                os.remove(p)


    def check_changes(self):
        repo = git.Repo(os.getcwd())

        diff = repo.index.diff(None)

        for item in diff:
            if 'src/' in item.a_path:
                ext = item.a_path.split('/')[1]
                self.publications[ext] = True

    def alloc_publications(self, check_changes=False):
        if check_changes:
            self.check_changes()
        else:
            for ext in os.listdir(self.SRC_DIR):
                if os.isdir(os.path.join(self.SRC_DIR, ext)):
                    self.publications[ext] = True


    def check_dependency(self):
        if not os.path.exists(f'{self.BLENDER}'):
            print(f'{self.BLENDER}')
            raise Exception("Blender not found. Configure Blender path in config.ini.")

        if not os.path.exists(self.SRC_DIR):
            raise Exception("Source directory lost. Repull repo.")

        os.makedirs(self.DST_DIR, exist_ok=True)


    def validate_manifest(self):
        cwd = os.getcwd()

        for ext in self.publications:
            src = os.path.join(self.SRC_DIR, ext)
            os.chdir(src)

            cmd = f'{self.BLENDER} --command extension validate'

            p = subprocess.Popen(cmd, shell=True, cwd=os.getcwd())

            p.wait()

            os.chdir(cwd)


    def validate_zip(self):
        cwd = os.getcwd()

        for ext in self.publications:
            dst = os.path.join(self.DST_DIR)
            os.chdir(dst)

            cmd = f'{self.BLENDER} --command extension validate {ext}-1.0.0-windows_x64.zip'

            p = subprocess.Popen(cmd, shell=True, cwd=os.getcwd())

            p.wait()

            os.chdir(cwd)


    def run(self):
        self.check_dependency()

        self.validate_manifest()

        self.alloc_publications(check_changes=False)

        self.cleanup()

        self.publish()

        self.validate_zip()

        print("===== FINISHED =====")

if __name__ == '__main__':
    publisher = extension_publisher()
    publisher.run()