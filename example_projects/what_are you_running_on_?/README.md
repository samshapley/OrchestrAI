# Comprehensive System Information Gathering Tool

## Overview
The System Information Gathering Tool is a powerful Python-based software that mines detailed information about your system's hardware and software. It captures data about the operating system, installed packages, and running processes. On the hardware end, it gathers information about your CPU, RAM, disk, and graphics.

These features come together to create a comprehensive snapshot of your system's status, useful for a variety of applications such as diagnostic testing, performance monitoring, or security auditing.

## Getting Started

### Prerequisites
Make sure to have Python installed on your system. In addition, the required Python packages listed in `requirements.txt` should be installed. They include:
- subprocess
- pkg_resources

You can install these packages using pip:

```sh
pip install -r requirements.txt
```

### Usage
The entry point for this application is `main.py`. Hence, you can run the tool using the following command:

```sh
python main.py
```

This will fetch and display system information in the console, as well as save this data into files under the 'my_mac' directory.

## Code Structure

The application is primarily divided into three modules: `hardware_info.py`, `software_info.py`, and `system_info.py`, each responsible for gathering a specific type of system information.

### HardwareInfo Module

This module defines the `HardwareInfo` class which gathers information about your hardware. It includes methods to extract details about your CPU, RAM, disk, and graphics card.

The data gathered by this module is written to JSON files (`cpu_info.json`, `ram_info.json`, `graphics_info.json`) and a CSV file (`disk_info.csv`) under 'my_mac' directory.

### SoftwareInfo Module

The `SoftwareInfo` class in this module collects detailed information about the software environment of your system. It fetches data regarding the operating system, installed packages, and running processes.

The information gathered here is saved into JSON files (`os_info.json`, `running_processes.json`) and a CSV file (`installed_packages.csv`) in the 'my_mac' directory.

### SystemInfo Module

The `SystemInfo` class brings together the `HardwareInfo` and `SoftwareInfo` classes to provide a unified interface for accessing all system information. It exposes the `get_info` method to print the system information to the console and the `save_info_to_files` method to write the data to files.

The `main.py` script creates an instance of `SystemInfo`, calls its methods to gather system information, and finally write the collected data to the appropriate files.