# lee lista de embeddings y calcula algunos cos similarity
# como la magnitud de los vectores es 1, el cos similarity es el producto punto
import csv
import math

def dot_product(vector1, vector2):
  # Calculates the dot product of two vectors.
  # Check that the vectors have the same size.
  if len(vector1) != len(vector2):
    raise ValueError("The two vectors must have the same size.")

  # Calculate the dot product.
  dot_product = sum(x * y for x, y in zip(vector1, vector2))

  return dot_product

# Define the file name and path where the CSV file is located
file_name = "vectores_de_animales.csv"

# Open the file in read mode
with open(file_name, mode='r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Convert the CSV data to a Python vector
    embeddings = []
    palabras = []
    magnitud = []
    for row in reader:
        # el ultimo item de cada lista es la palabra que da lugar al embedding
        # la saco y la dejo en un arreglo distinto
        palabra = row.pop()
        palabras.append(palabra) 
        # cada fila tiene solo los embeddings
        # los lee en forma de string asi que los convierto a float
        float_row = [float(x) for x in row]
        magnitud.append(math.sqrt(sum(x ** 2 for x in float_row)))
        embeddings.append(float_row)

# al finalizar el loop, existen dos listas:
# palabras[] cada item tiene la palabra que da origen al embedding
# embeddings[] cada item es el embedding de más de 1000 posiciones

for i in range(1,len(embeddings)):
   print(i-1, palabras[i-1], magnitud[i-1])

i = 1
j = 6
print(palabras[i], embeddings[i][0], embeddings[i][-1])
print(palabras[j], embeddings[j][0], embeddings[j][-1])

producto_punto = dot_product(embeddings[i], embeddings[j])

print(producto_punto)

