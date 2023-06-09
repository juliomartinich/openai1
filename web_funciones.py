from flask import Flask, render_template, request, redirect, session
import sys, os, openai, csv
import time
from datetime import datetime
#----------------------------------------------------------------
# esta version toma el contenido anterior y posterior para el prompt
# ademas intenta una defensa de prompt injection 
# sacando signos de puntuacion
# agrego un login simple
# agrego escritura  basica en csv
# agrego timestamp al csv de preguntas
#-----------------------------------------------------------------
def escribir_en_archivo_csv(vector, pregunta, respuesta, imc, pc_mas_cercano, nombre_archivo):
    existe_archivo = os.path.isfile(nombre_archivo)
    with open(nombre_archivo, 'a', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)

        registro = vector
        usuario = session.get('username')
        registro.append(usuario)
        timestamp = int(time.time())
        formatted_time = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
        registro.append(formatted_time)
        registro.append(pregunta)
        registro.append(respuesta)
        registro.append(imc)
        registro.append(pc_mas_cercano)
        writer.writerow(registro)  # Escribe la fila adicional en el archivo existente

#-----------------------------------------------------------------
def eliminar_signos_especiales(cadena):
    """
    Esta función elimina todos los signos especiales de un string 
    utilizando un ciclo for y la función isalnum().
    """
    cadena_sin_signos = ""
    for caracter in cadena:
        if caracter.isalnum() or caracter.isspace():
            cadena_sin_signos += caracter
    return cadena_sin_signos

#--------------------------------
def read_embedding(texto):
  # esta funcion se usa acá para obtener el embedding de la pregunta aislada
  vector_embedding = openai.Embedding.create(
    input=texto, model="text-embedding-ada-002"
    )["data"][0]["embedding"]

  return vector_embedding

#--------------------------------
def dot_product(vector1, vector2):
  # se usa para calcular la similitud de los embeddings
  # Calculates the dot product of two vectors.
  # Check that the vectors have the same size.
  if len(vector1) != len(vector2):
    raise ValueError("The two vectors must have the same size.")

  # Calculate the dot product.
  dot_product = sum(x * y for x, y in zip(vector1, vector2))

  return dot_product

#--------------------------------
def read_stored_embeddings(file_name):
  # lee los embeddings almacenados en un archivo csv
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
  # embeddings[] cada item es el embedding de más de 1500 posiciones
  return parrafos, archivos, textos, embeddings

#--------------------------------
def busca_contexto(vector, embeddings, textos):
# busca el parrafo mas cercano a la pregunta 
# usando el vector embedding de la pregunta

  mas_cercano = -1
  segundo_mas_cercano = -1
  imc = 0
  for i in range(len(embeddings)):
    resultado = dot_product(vector, embeddings[i])
    if resultado > mas_cercano:
      segundo_mas_cercano = mas_cercano
      ismc = imc
      mas_cercano = resultado
      imc = i
    elif resultado > segundo_mas_cercano and resultado != mas_cercano:
      segundo_mas_cercano = mas_cercano
      ismc = i
  
  pc_mas_cercano = round( 100 * mas_cercano, 1)
  pc_segundo_mas_cercano = round( 100 * segundo_mas_cercano, 1)
  # despues de este loop imc tiene el indice del mas cercano

  contexto = textos[imc] + "    \n /      " + textos[ismc]

  return contexto, imc, pc_mas_cercano

#--------------------------------
def get_answer(pregunta, embeddings, textos, archivos):
#-- lee el vector embedding de la pregunta
#-- calcula el texto mas cercano
#-- en base a la pregunta y los textos mas cercanos
#-- construye un prompt para que se responda la pregunta

  vector = read_embedding(pregunta)

  ( contexto, imc , pc_mas_cercano) = busca_contexto(vector, embeddings, textos)

  prompt_prologo = "Basado en la siguiente informacion: "
  prompt_post    = " Responde la siguiente pregunta en pocas palabras: ¿ "
  prompt_post_2  = "  ? Si con la informacion proporcionada no se puede \
                     responder la pregunta, responde <EOF>"

  prompt = prompt_prologo \
         + contexto       \
         + prompt_post    \
         + eliminar_signos_especiales(pregunta)       \
         + prompt_post_2    

  mensaje ={}
  mensaje["role"]="user"
  mensaje["content"]=prompt

  chatprompt=[]
  chatprompt.append(mensaje)

  # esta version usa gpt-3.5-turbo, que es mas barato que davinci
  respuesta = openai.ChatCompletion.create(
         messages = chatprompt,
         model  = "gpt-3.5-turbo",
         max_tokens = 300,
         temperature = 0
  )["choices"][0]["message"]["content"]

  # salvo la pregunta, su embedding y respuesta en un csv
  escribir_en_archivo_csv(vector, pregunta, respuesta, imc, pc_mas_cercano, "preguntas.csv")

  if "EOF" in respuesta:
     respuesta = "No puedo responder la pregunta con la información entregada"

  return respuesta, archivos[imc], contexto, prompt, pc_mas_cercano

#----------------------------------------------------
