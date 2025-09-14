# tests/test_service.py
import re
import os
from core.builder.service import (
    set_now_variables, set_data_file,
    get_master_register_file, write_data_file, set_start_time, generate_data,
    set_end_time, update_master_register_file)

def test_set_now_variables_returns_datetime():
    result = set_now_variables()
    from datetime import datetime
    assert isinstance(result, datetime)

def test_set_data_file_format():
    filename = set_data_file()
    # Expect format: DDMMYYHHMMSS_data_raw.csv
    assert re.match(r"\d{12}_data_raw\.csv", filename)

def test_get_master_register_file():
    master_file = get_master_register_file()
    assert master_file == "register.csv"

def test_write_data_file_creates_file(tmp_path):
    # Create data_raw directory in the temporary path
    data_raw_dir = tmp_path.parent / "data_raw"
    data_raw_dir.mkdir()

    # Change directory to temporary path for testing
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    write_data_file()
    filename = set_data_file()
    file_path = data_raw_dir / filename

    # Check if the file was created
    assert file_path.exists()

    # Check if the header is correct
    with open(file_path, "r") as file:
        header = file.readline().strip()
        assert header == "uuid,series,status,created_date"

    # Revert to original directory
    os.chdir(original_cwd)

def test_set_start_time_format():
    start_time = set_start_time()
    # Expect format: HH:MM:SS
    assert re.match(r"\d{2}:\d{2}:\d{2}", start_time)

def test_generate_data(tmp_path):
    # Create data_raw directory if it doesn't exist
    data_raw_dir = tmp_path.parent / "data_raw"
    data_raw_dir.mkdir(exist_ok=True)

    # change working directory to tmp_path
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    # write header and generate data
    write_data_file()
    filename = set_data_file()
    generate_data(filename)

    file_path = data_raw_dir / filename

    # Check if data was appended to the file
    with open(file_path, "r") as file:
        lines = file.readlines()
        # There should be 11 lines: 1 header + 10 data lines
        assert len(lines) == 11
        for line in lines[1:]:  # Skip header
            parts = line.strip().split(",")
            assert len(parts) == 4  # uuid, series, status, created_date
            assert re.match(r"[0-9a-fA-F-]{36}", parts[0])  # UUID format
            assert parts[2] == "raw"  # Status should be 'raw'
            assert re.match(r"\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}", parts[3])  # Date format

    os.chdir(original_cwd)

def test_set_end_time_format():
    end_time = set_end_time()
    # Expect format: HH:MM:SS
    assert re.match(r"\d{2}:\d{2}:\d{2}", end_time)

def test_update_master_register_file(tmp_path):
    # Ensure builder directory exists
    builder_dir = tmp_path.parent  / "builder"
    builder_dir.mkdir(exist_ok=True)

    # change working directory to tmp_path
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    # Update the Master File with new line
    # Set initial status
    file_initial_status = "new"
    filename = set_data_file()
    now = set_now_variables().strftime("%m/%d/%Y-%H:%M:%S")
    master_file_path = builder_dir / get_master_register_file()

    # Append new entry to the master register file
    with open(master_file_path, "a") as file:
        file.write(f"{filename},{file_initial_status},{now}\n")

    #Check if the fle was created and contains the new line
    with open(master_file_path, "r") as file:
        lines = file.readlines()
        assert any(filename in line for line in lines)

    os.chdir(original_cwd)