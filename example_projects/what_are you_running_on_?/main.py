from system_info import SystemInfo

def main():
    info = SystemInfo()
    info.get_info()
    info.save_info_to_files()

if __name__ == "__main__":
    main()
