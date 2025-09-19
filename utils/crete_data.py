import csv
import random

def create_csv_data(number_of_data: int, filename: str="track.csv") -> None:
    # Define CSV file name and header

    header = ['trackID', 'X', 'Y', 'V_X', 'V_Y']

    # Generate 10,000 rows of random data
    data = []
    for track_id in range(1, number_of_data + 1):  # trackID from 1 to 10,000
        row = [
            track_id,  # Integer trackID
            random.uniform(1, 1000),  # X coordinate in meters
            random.uniform(1, 1000),  # Y coordinate in meters
            random.uniform(1, 100),    # V_X in m/s
            random.uniform(1, 100)     # V_Y in m/s
        ]
        data.append(row)

    # Write data to CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)
    print(f"CSV file '{filename}' with 10,000 entries has been created.")

if __name__ == "__main__":
    create_csv_data(number_of_data=900001)