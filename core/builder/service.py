import random
import numpy
import uuid
import csv
from datetime import datetime

# Variable to store the time at the start of the process
def set_now_variables():
    str_now  = datetime.now()
    return str_now

def set_data_file():
    str_date_time = set_now_variables().strftime("%d%m%y%H%M%S")
    return str_date_time + "_data.csv"

def get_master_register_file():
    return "register.csv"

# create data file as .csv  that store the series of numbers
# the format of the file name is [date-time]_data.csv
def write_data_file():
    with open("../data/" + set_data_file(), "w") as file:
        writer = csv.writer(file)
        writer.writerow(["uuid","series","status","created_date"])

write_data_file()
filename = set_data_file()

#Get the time when the process start
def set_start_time():
    return set_now_variables().strftime("%H:%M:%S")

# Generate a list of random numbers (duplicates allowed)
def generate_data():
    j = 1
    n = 5
    n_series = 10
    # Open file to store series of numbers
    file = open("../data/" + filename, "a")

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

#Get the time when the process finished
def set_end_time():
    return set_now_variables().strftime("%H:%M:%S")

# Update Master File that keep register
# of new Files generated
def update_master_register_file():
    # Set initial status
    file_initial_status = "new"
    #open the master file
    register_file = open(get_master_register_file(), "a")
    #update the master by input new line
    register_file.write(filename+","+set_now_variables().strftime("%d/%m/%Y")+","+file_initial_status+","+set_start_time()+","+set_end_time()+"\n" )

generate_data()
update_master_register_file()
