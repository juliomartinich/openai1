import openai, os

openai.api_key = os.environ.get('OPENAIAPIKEY')

palabras = ["gato", "perro"]
#, "burro", "cisne", "zorro", "liebre", "caballo", "nutria", "coipo" ]

vectores = {}
for palabra in palabras:
  vectores[palabra] = openai.Embedding.create(
    input=palabra, model="text-embedding-ada-002"
  )["data"][0]["embedding"]

palabra="perro"
print( len(vectores[palabra]), "  ", vectores[palabra][0] )

