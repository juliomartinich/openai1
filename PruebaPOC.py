import requests
from bs4 import BeautifulSoup

# URL de la página web
url = 'http://34.145.131.242:5000/'

# Credenciales de inicio de sesión
username = 'nicolas'
password = 'pepelon'

# Archivo de entrada con las preguntas
archivo_entrada = 'preguntas.txt'

# Archivo de salida para las respuestas
archivo_salida = 'respuestas.txt'

# Realizar la solicitud de inicio de sesión
login_data = {
    'username': username,
    'password': password
}
session = requests.Session()
session.post(url, data=login_data)

# Abrir el archivo de entrada y leer las preguntas
with open(archivo_entrada, 'r') as file:
    preguntas = file.read().splitlines()

# Realizar solicitudes para cada pregunta y guardar las respuestas en el archivo de salida
with open(archivo_salida, 'w') as file:
    for pregunta in preguntas:
        # Realizar la solicitud con la pregunta
        response = session.post(url, data={'pregunta': pregunta})
        
        # Analizar la respuesta HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer la pregunta y la respuesta del HTML
        #pregunta_html = soup.find('p', class_='pregunta').text.strip()
        #respuesta_html = soup.find('p', class_='respuesta').text.strip()
		# Extraer la pregunta y la respuesta del HTML
        pregunta_element = soup.find('p', class_='pregunta')
        respuesta_element = soup.find('p', class_='respuesta')

		# Verificar si se encontraron los elementos
        if pregunta_element and respuesta_element:
           pregunta_html = pregunta_element.text.strip()
           respuesta_html = respuesta_element.text.strip()
    
		# Escribir la pregunta y la respuesta en el archivo de salida
           file.write(f'{pregunta_html}\t{respuesta_html}\n')
        else:
           print(f"No se pudo encontrar la pregunta y la respuesta para la pregunta: {pregunta}")
        
        # Escribir la pregunta y la respuesta en el archivo de salida
        #file.write(f'{pregunta_html}\t{respuesta_html}\n')

print("¡Pruebas completadas! Las respuestas se han guardado en el archivo 'respuestas.txt'.")
