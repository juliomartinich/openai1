import requests

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

# Iniciar sesión y obtener las cookies
cookies = login('nicolas', 'pepelon')

# Realizar la pregunta a OpenAI GPT
question = '¿La Cédula de Identidad se puede reemplazar por la colilla que entrega el Registro Civil?'
response_text = get_openai_response(cookies, question)

# Mostrar la respuesta en la pantalla
print(response_text)
