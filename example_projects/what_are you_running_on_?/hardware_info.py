import subprocess
import csv
import json
import os

class HardwareInfo:
    def get_cpu_info(self):
        cpu_info = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).strip()
        cpu_cores = subprocess.check_output(["sysctl", "-n", "hw.ncpu"]).strip()
        return f"CPU: {cpu_info.decode()}, Cores: {cpu_cores.decode()}"

    def get_ram_info(self):
        total_mem = subprocess.check_output(["sysctl", "-n", "hw.memsize"]).strip()
        return f"RAM: {int(total_mem) / (1024 * 1024 * 1024)} GB"

    def get_disk_info(self):
        disk_info = subprocess.check_output(["df", "-h"]).strip()
        return disk_info.decode()

    def get_graphics_info(self):
        graphics_info = subprocess.check_output(["system_profiler", "SPDisplaysDataType"]).strip()
        return graphics_info.decode()

    def write_data_to_files(self):
        if not os.path.exists('my_mac'):
            os.makedirs('my_mac')

        with open('my_mac/cpu_info.json', 'w') as f:
            json.dump(self.get_cpu_info(), f)

        with open('my_mac/ram_info.json', 'w') as f:
            json.dump(self.get_ram_info(), f)

        with open('my_mac/disk_info.csv', 'w') as f:
            f.write(self.get_disk_info())

        with open('my_mac/graphics_info.json', 'w') as f:
            json.dump(self.get_graphics_info(), f)
