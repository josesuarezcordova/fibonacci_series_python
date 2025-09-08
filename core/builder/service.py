import random
import numpy
import uuid
from datetime import datetime

# Variable to store the time at the start of the process
str_now  = datetime.now()

def get_master_register_file():
    return("register.csv")

# create data file as .csv  that store the series of numbers
# the format of the file name is [date-time]_data.csv
def set_data_file(str_now):
    str_date_time = str_now.strftime("%d%m%y%H%M%S")
    filename = str_date_time+"_data.csv"
    file = open("../data/" + filename, "w")
    file.write("uuid,series,status,created_date\n")
    return filename

#set filename
filename = set_data_file(str_now)

#Get the time when the process start
start_time = str_now.strftime("%H:%M:%S")

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
end_time = str_now.strftime("%H:%M:%S")

# Update Master File that keep register
# of new Files generated
def update_master_register_file(start_time,end_time):
    # Set initial status
    file_initial_status = "new"
    #open the master file
    register_file = open(get_master_register_file(), "a")
    #update the master by input new line
    register_file.write(filename+","+str_now.strftime("%d/%m/%Y")+","+file_initial_status+","+start_time+","+end_time+"\n" )

generate_data()
update_master_register_file(start_time,end_time)
