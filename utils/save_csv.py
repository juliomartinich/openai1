import csv

# Define the vector
my_vector = [1, 2, 3, 4, 5]

# Define the file name and path where you want to save the CSV file
file_name = "my_vector.csv"

# Open the file in write mode
with open(file_name, mode='w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write the vector to the file
    writer.writerow(my_vector)

