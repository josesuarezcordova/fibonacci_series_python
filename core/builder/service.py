import random
import numpy
import uuid
import csv
from datetime import datetime

def set_now_variables():
    # set the current date and time
    str_now  = datetime.now()
    return str_now

def set_data_file():
    # set the name of the file with date-time format
    str_date_time = set_now_variables().strftime("%d%m%y%H%M%S")
    return str_date_time + "_data_raw.csv"

def get_master_register_file():
    # get the path of the Master File
    return "register.csv"

def write_data_file():
    # Write the header of the file
    with open("../data_raw/" + set_data_file(), "w") as file:
        writer = csv.writer(file)
        writer.writerow(["uuid","series","status","created_date"])

write_data_file()
filename = set_data_file()

def set_start_time():
    # Get the time when the process start
    return set_now_variables().strftime("%H:%M:%S")

# Generate a list of random numbers (duplicates allowed)
def generate_data():
    # Generate series of 5 random numbers between 0 and 10
    j = 1
    n = 5
    n_series = 10
    # Open file to store series of numbers
    file = open("../data_raw/" + filename, "a")

    while j <= n_series:
        now = datetime.now()
        series_created_date = now.strftime("%m/%d/%Y-%H:%M:%S")
        series_uuid = str(uuid.uuid4())
        li = [random.randint(0, 10) for _ in range(n)]
        series = str(numpy.array(li))
        print(series)
        file.write(str(series_uuid)+","+series+",raw,"+ series_created_date+"\n")
        j += 1
    file.close()

generate_data()

def set_end_time():
    # get the time when the process finished
    return set_now_variables().strftime("%H:%M:%S")

def update_master_register_file():
    # Update the Master File with new line
    # Set initial status
    file_initial_status = "new"
    register_file = open(get_master_register_file(), "a")
    register_file.write(filename+","+set_now_variables().strftime("%d/%m/%Y")+","+file_initial_status+","+set_start_time()+","+set_end_time()+"\n" )

update_master_register_file()
