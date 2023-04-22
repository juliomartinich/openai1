import csv

# Define the file name and path where the CSV file is located
file_name = "my_vector.csv"

# Open the file in read mode
with open(file_name, mode='r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Convert the CSV data to a Python vector
    rows = []
    for row in reader:
        rows.append(row)

# Print the vector to verify it was read correctly
for i in range(0,3):
    print(rows[i])
