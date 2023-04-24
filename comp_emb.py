# operaciones leyendo vectores embeddings guardados en un archivo csv
def dot_product(vector1, vector2):
  # Calculates the dot product of two vectors.
  # Check that the vectors have the same size.
  if len(vector1) != len(vector2):
    raise ValueError("The two vectors must have the same size.")

  # Calculate the dot product.
  dot_product = sum(x * y for x, y in zip(vector1, vector2))

  return dot_product

def read_stored_embeddings(file_name):
  import csv

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
        palabras.append(palabra) 
        # cada fila tiene solo los embeddings
        # los lee en forma de string asi que los convierto a float
        float_row = [float(x) for x in row]
        embeddings.append(float_row)

  # al finalizar el loop, existen dos listas:
  # palabras[] cada item tiene la palabra que da origen al embedding
  # embeddings[] cada item es el embedding de más de 1000 posiciones

  return palabras, embeddings

# ---------------------------------------------------------------------------
# acá empieza el main
# lee lista de embeddings y calcula algunos cos similarity
# como la magnitud de los vectores es 1, el cos similarity es el producto punto

# Define the file name and path where the CSV file is located
vectores = read_stored_embeddings(file_name = "vectores_de_animales.csv")
palabras   = vectores[0]
embeddings = vectores[1]

print(len(palabras), len(embeddings))
print("------ ")

for i in range(len(embeddings)):
  print(i, palabras[i])
print("------ ")

mas_cerca = 0
mas_lejos = 1
for i in range(len(embeddings)):
  for j in range(i,len(embeddings)):
    punto = 1 if i==j else dot_product(embeddings[i],embeddings[j])
    print(palabras[i], palabras[j], punto)
    if i != j :
      if punto > mas_cerca :
        mas_cerca = punto
        i_mc = i
        j_mc = j
      if punto < mas_lejos :
        mas_lejos = punto
        i_ml = i
        j_ml = j

print(" ---- mas cercanos ---")
print(palabras[i_mc], palabras[j_mc], mas_cerca)
print(" ---- mas lejanos ---")
print(palabras[i_ml], palabras[j_ml], mas_lejos)

