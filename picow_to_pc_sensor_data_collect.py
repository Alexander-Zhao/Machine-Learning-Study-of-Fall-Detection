# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 00:11:46 2024

@author: mingzh
"""

import serial  # Import the pyserial library
import time

# Set up the serial connection
ser = serial.Serial('COM4', baudrate=1500000, timeout=1)

# Path to the file where data will be saved
file_path = r"C:\Users\mingzh\fall_detection\Fall_Test\OtherTesters\yangyang\f09_raw_data_05.txt"
#file_path = r"C:\Users\mingzh\fall_detection\Fall_Test\f01_raw_data_06.txt"

# Variables to store timestamps and start time
first_timestamp = None
last_timestamp = None
start_time = None

# Duration in seconds (adjustable)
duration_limit = 15  # Change this value to your desired duration

try:
    # Open the file in append mode
    with open(file_path, 'a') as file:
        print("Reading from serial port and writing to file...")
        
        # Record the start time
        start_time = time.time()

        while True:
            # Check elapsed time
            elapsed_time = time.time() - start_time
            if elapsed_time >= duration_limit:
                print("Duration limit reached. Stopping the program...")
                break
            
            # Read a line from the serial port
            try:
                data = ser.readline().decode('utf-8').strip()  # Decode and strip newline characters
            except UnicodeDecodeError:
                print("Error decoding data from serial port")
                continue

            # Check if there's data to write
            if data:
                # Capture the first timestamp
                if first_timestamp is None:
                    first_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print(f"First timestamp: {first_timestamp}")
                    file.write(f"First Timestamp: {first_timestamp}\n")  # Write first timestamp to file
                
                # Write data to the file
                print(f"Received: {data}")
                file.write(data + '\n')
                
                # Update the last timestamp
                last_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # Optional delay to prevent high CPU usage
            #time.sleep(0.1)

except serial.SerialException as e:
    print(f"Serial error: {e}")

except IOError as e:
    print(f"File I/O error: {e}")

except KeyboardInterrupt:
    print("Program interrupted. Exiting...")

finally:
    # Write the last timestamp and total time interval to the file before closing
    if last_timestamp:
        end_time = time.time()  # Record the end time in seconds
        duration = end_time - start_time  # Calculate the total duration
        print(f"Last timestamp: {last_timestamp}")
        print(f"Total duration (seconds): {duration:.2f}")
        
        with open(file_path, 'a') as file:
            file.write(f"Last Timestamp: {last_timestamp}\n")  # Write last timestamp to file
            file.write(f"Total Duration (seconds): {duration:.2f}\n")  # Write total duration to file

    # Close the serial connection
    if ser.is_open:
        ser.close()
    print("Serial connection closed.")
