# lee vectores embeddings guardados en un archivo csv
# pide que se ingrese un texto, calcula su embedding y busca cual es el mas cercano
# con ese mas cercano openai construye la respuesta 

def read_embedding(texto):

  vector_embedding = openai.Embedding.create(
    input=texto, model="text-embedding-ada-002"
  )["data"][0]["embedding"]

  return vector_embedding

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
    textos = []
    archivos = []
    parrafos = []
    for row in reader:
        # el ultimo item de cada lista es el texto que da lugar al embedding
        # la saco y la dejo en un arreglo distinto
        texto = row.pop()
        textos.append(texto) 
        # el siguiente desde atras es el nombre del archivo
        nombre_archivo = row.pop()
        archivos.append(nombre_archivo)
        # y el siguiente desde atras es el numero del parrafo de la indexacion
        nro_parrafo = row.pop()
        parrafos.append(nro_parrafo)
        # ahora cada fila tiene solo los embeddings
        # los lee en forma de string asi que los convierto a float
        float_row = [float(x) for x in row]
        embeddings.append(float_row)

  # al finalizar el loop, existen cuatro listas:
  # parrafos[]
  # archivos[]
  # textos[] cada item tiene el texto que da origen al embedding
  # embeddings[] cada item es el embedding de más de 1000 posiciones

  return parrafos, archivos, textos, embeddings

# ---------------------------------------------------------------------------
# acá empieza el main
# lee lista de embeddings y calcula algunos cos similarity
# como la magnitud de los vectores es 1, el cos similarity es el producto punto

import sys, openai, os

openai.api_key = os.environ.get('OPENAIAPIKEY')

vectores = read_stored_embeddings(file_name = "mis_word_embed.csv")
parrafos   = vectores[0]
archivos   = vectores[1]
textos     = vectores[2]
embeddings = vectores[3]

print(" ")

print("-- textos leidos --")
for i in range(len(embeddings)):
  print(i, textos[i][0:90])

print("\nIngrese una pregunta y le respondere en base al texto mas cercano : ")
texto_a_buscar = input()
vector = read_embedding(texto_a_buscar)

mas_cercano = -1
imc = 0
resultados = []
for i in range(len(embeddings)):
  resultado = dot_product(vector, embeddings[i])
  resultados.append(resultado)
  if resultado > mas_cercano:
    mas_cercano = resultado
    imc = i

print(" ")
print("mas cercano = ", mas_cercano)
print(textos[imc])
print(imc, archivos[imc])
print(" ")

prompt_prologo = "Por favor responde la siguiente pregunta: "
prompt_epilogo = " basado estrictamente en la informacion que te doy a continuacion "
prompt_post    = "; en el caso en que no este relacionado, responde: No tengo esa informacion.  Aca va la informacion que debes usar en caso de estar relacionados (recuerda usar solamente esta informacion para responder): "

prompt = prompt_prologo + texto_a_buscar + prompt_epilogo + prompt_post + textos[imc]

respuesta = openai.Completion.create(
       prompt = prompt,
       model  = "text-davinci-003",
       max_tokens = 1000,
       temperature = 0
)["choices"][0]["text"]

print(" ")
print("respuesta de IA = ", respuesta)
print(" ")


