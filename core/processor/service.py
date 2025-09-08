import os
import time
import sort_services as sort_service

#Open Master Register File
def open_register_file(file_path):
    print("opening master file")
    with open(file_path) as f:
        for line in f:
            pass
        last_line = line

        string_last_line = last_line.split(",")
        last_file_created = string_last_line[0]

        sort_service.sort_array_series(str(last_file_created))

#Check update Master File
def detect_master_file_changes(file_path, interval=1):
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        # Confirm the file was modified
        if current_modified != last_modified:
            print("File has changed!")
            last_modified = current_modified
            # Open the last file created
            open_register_file(file_path)
        time.sleep(interval)

#Call the function passing the path of the Master File
detect_master_file_changes("../builder/register.csv")


