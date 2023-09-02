import subprocess
import pkg_resources
import csv
import json
import os

class SoftwareInfo:
    def get_os_info(self):
        os_info = subprocess.check_output(["sw_vers"]).strip()
        return os_info.decode()

    def get_installed_packages(self):
        installed_packages = [str(d) for d in pkg_resources.working_set]
        return installed_packages

    def get_running_processes(self):
        running_processes = subprocess.check_output(["ps", "aux"]).strip()
        return running_processes.decode()

    def write_data_to_files(self):
        if not os.path.exists('my_mac'):
            os.makedirs('my_mac')

        with open('my_mac/os_info.json', 'w') as f:
            json.dump(self.get_os_info(), f)

        with open('my_mac/installed_packages.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.get_installed_packages())

        with open('my_mac/running_processes.json', 'w') as f:
            json.dump(self.get_running_processes(), f)
