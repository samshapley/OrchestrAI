from hardware_info import HardwareInfo
from software_info import SoftwareInfo

class SystemInfo:
    def __init__(self):
        self.hardware_info = HardwareInfo()
        self.software_info = SoftwareInfo()

    def get_info(self):
        print("Hardware Information: ")
        print(self.hardware_info.get_cpu_info())
        print(self.hardware_info.get_ram_info())
        print(self.hardware_info.get_disk_info())
        print(self.hardware_info.get_graphics_info())

        print("\nSoftware Information: ")
        print(self.software_info.get_os_info())
        print(self.software_info.get_installed_packages())
        print(self.software_info.get_running_processes())

    def save_info_to_files(self):
        self.hardware_info.write_data_to_files()
        self.software_info.write_data_to_files()
