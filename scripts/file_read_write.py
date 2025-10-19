import csv

def read_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            print(row)

def write_csv(file_path, data):
    with open(file_path, mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data)

# Input and Output
file_path = input("Enter CSV file path: ")
print("\nReading CSV File:")
read_csv(file_path)

new_data = input("\nEnter data to write (comma separated): ").split(',')
write_csv(file_path, new_data)
print("Data written successfully!")
