import requests
from bs4 import BeautifulSoup

def login(username, password):
    login_url = 'http://34.145.131.242:5000/login'
    data = {'username': username, 'password': password}
    response = requests.post(login_url, data=data)
    return response.cookies

def get_openai_response(cookies, question):
    index_url = 'http://34.145.131.242:5000/submit'
    data = {'fpregunta': question}
    response = requests.post(index_url, data=data, cookies=cookies)
    return response.text

def process_questions(username, password, input_file, output_file):
    # Iniciar sesión y obtener las cookies
    cookies = login(username, password)

    # Leer las preguntas desde el archivo de entrada
    with open(input_file, 'r') as file:
        questions = file.read().splitlines()

    # Procesar cada pregunta y guardar las respuestas en el archivo de salida
    with open(output_file, 'w') as file:
        file.write('Pregunta,Respuesta\n')
        for question in questions:
            # Realizar la pregunta a OpenAI GPT
            response_text = get_openai_response(cookies, question)

            # Parsear el HTML de la respuesta
            soup = BeautifulSoup(response_text, 'html.parser')
            respuesta_tag = soup.find('p', class_='respuesta')

            if respuesta_tag:
                respuesta_text = respuesta_tag.text.strip()
            else:
                respuesta_text = 'No se encontró respuesta'

            # Guardar la pregunta y la respuesta en el archivo de salida
            file.write(f'"{question}","{respuesta_text}"\n')

    print(f"Las respuestas se han guardado en el archivo: {output_file}")

# Parámetros de configuración
username = 'nicolas'
password = 'pepelon'
input_file = 'preguntas.txt'
output_file = 'respuestas.csv'

# Procesar las preguntas y guardar las respuestas en el archivo de salida
process_questions(username, password, input_file, output_file)
