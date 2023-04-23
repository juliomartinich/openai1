# lee lista de embeddings

import csv

# Define the file name and path where the CSV file is located
file_name = "vectores_de_animales.csv"

# Open the file in read mode
with open(file_name, mode='r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Convert the CSV data to a Python vector
    embeddings = []
    palabras = []
    for row in reader:
        # el ultimo item de cada lista es la palabra que da lugar al embedding
        # la saco y la dejo en un arreglo distinto
        palabra = row.pop()
        print(palabra)
        palabras.append(palabra) 
        # cada fila tiene solo los embeddings
        embeddings.append(row)

# Print the first item in each  vector to verify it was read correctly
for row in embeddings:
    print(row[0])


