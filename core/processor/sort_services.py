import csv

filas = []
def sort_array_series(file):
    print("opening last file of series created")
    series_file = "../data/" + file

    with open(series_file) as f:
        for line in f:
            print(line)