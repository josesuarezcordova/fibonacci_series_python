import os
import time
import data_services as data_services

def open_register_file(file_path):
    # Open the master file and read the last line
    print("opening master file")
    with open(file_path) as f:
        for line in f:
            pass
        last_line = line

        string_last_line = last_line.split(",")
        last_file_created = string_last_line[0]
        print(last_file_created)

        data_services.start_validation_series(str(last_file_created))

def detect_master_file_changes(file_path, interval=1):
    # detect changes in the master file
    print("detecting changes in the master file")
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


