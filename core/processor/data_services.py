import re
import csv
import shutil
from datetime import datetime

# Variable to store the time at the start of the process
def set_now_variables():
    # Set the current date and time
    str_now  = datetime.now()
    return str_now

def set_new_data_file():
    # Create a new file name with date-time format
    str_date_time = set_now_variables().strftime("%d%m%y%H%M%S")
    with open("../data_sorted/" + set_new_data_file(), "w") as file:
        writer = csv.writer(file)
        writer.writerow(["uuid","series","status","created_date"])

    return str_date_time + "_data_sorted.csv"

def write_new_data_file(data, sorted_numbers):
    # Write the sorted series to the new file
    file_sorted_status = "sorted"
    with open("../data_sorted/" + set_new_data_file(), "w") as file:
        writer = csv.writer(file)
        writer.writerow([data[0], str(sorted_numbers), file_sorted_status, data[3].strip()])

def check_len(series_numbers):
    # Check if the series has exactly 5 numbers
    if len(series_numbers) != 5:
        raise ValueError("Series must contain exactly 5 numbers.")
    return True

def check_number_range(series_numbers):
    # Check if all numbers are between 0 and 10
    for num in series_numbers:
        if num < 0 or num > 10:
            raise ValueError("Numbers must be between 0 and 10.")
    return True

def check_no_empty(series_numbers):
    # Check if there are empty values in the line
    if "" in series_numbers:
        raise ValueError("Line contains empty values.")
    return True

def check_integrity(series_numbers):
    # Run all validation checks
    try:
        check_len(series_numbers)
        check_number_range(series_numbers)
        check_no_empty(series_numbers)
        return True
    except ValueError as e:
        print(f"Validation error: {e}")
        return False

def start_validation_series(file):
    # Sort the array of numbers in ascending order
    series_file = "../data_raw/" + file
    shutil.copyfile(series_file, "../data_sorted/" + file)
    print("File copied")
    update_sorted_file("../data_sorted/" + file)

def update_sorted_file(file_path):
    # Update the sorted file with sorted series
    lines = []
    # Read the CSV file (skip header), validate and sort the number series in each line,
    # update the series and status, then store the modified lines for later writing.
    with open(file_path, 'r') as f:
        next(f)
        for line in f:
            data = line.split(",")
            s = data[1]
            numbers = [int(num) for num in re.findall(r'\d+', s)]

            if check_integrity(numbers):
                sorted_numbers = sorted(numbers)

                parts = line.strip().split(',')
                if len(parts) > 1:
                    parts[1] = str(sorted_numbers)
                    parts[2] = "sorted"
                lines.append(','.join(parts))

    with open(file_path, 'r') as f:
        header = f.readline()

    with open(file_path, 'w') as f:
        f.write(header)
        writer = csv.writer(f)
        for line in lines:
            f.write(line + '\n')





