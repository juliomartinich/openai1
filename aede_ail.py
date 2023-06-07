from flask import Flask, render_template, request, redirect, session, jsonify
import os, openai, logging, datetime, traceback
import web_funciones as wf
import json

def inicia_chat():
   chat = []  # Reinicia la variable de conversación

   prompt = """
Eres un asistente de una aerolinea, tu misión es obtener ciudad de origen y destino, y fechas de ida y vuelta, preguntando al cliente.  Cada vez que obtengas un dato debes entregar una respuesta en formato JSON al finalizar la respuesta normal.  Hoy es martes 6 de Junio de 2023, si te piden una fecha en forma relativa dedúcela a partir de hoy usando el calendario.
---
ejemplo 1: Quiero viajar a Santiago

Entiendo que quiere viajar a Santiago, ¿desde que ciudad de origen?

JSON {"origen": "Valdivia", "destino":"Santiago", "fecha ida":"", "fecha vuelta":""}
---

ejemplo 2: Quiero viajar el primer martes de septiembre

de acuerdo, como el 1ro de septiembre cae viernes, sería el 5 de septiembre, ¿desde donde desea viajar?

JSON {"origen": "", "destino":"", "fecha ida":"05-09-2023", "fecha vuelta":""}
---

   """
   chat.append({"role": "user", "content": prompt})

   logging.info("Prompt: " + prompt)

   return chat

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')
app.secret_key = openai.api_key  # API openai de clave secreta para la sesión

#configura logging
logging.basicConfig(filename='aede.log', level=logging.INFO)

# Variable global para mantener el contexto de la conversación
conversacion = inicia_chat()


#-------------------------@
@app.errorhandler(404)
def page_not_found(error):
    # Aquí puedes personalizar la respuesta para las rutas no encontradas
    return render_template('404.html'), 404

#-------------------------@
# Manejador de errores personalizado
@app.errorhandler(Exception)
def handle_error(e):
    # Captura información del error
    error_message = f'Ocurrió un error inesperado: {str(e)}'
    error_traceback = traceback.format_exc()

    # Registra el error en el archivo de registro
    logging.error(error_message)
    logging.error(error_traceback)

    return 'Se ha producido un error inesperado.', 500

#-------------------------@
@app.before_request
def log_request_info():
    # Registra la información de la solicitud HTTP
    logging.info('Request URL: %s RemoteIP: %s', request.url, request.remote_addr)
    #logging.info('Request method: %s', request.method)
    #logging.info('Request headers: %s', request.headers)
    #logging.info('Request data: %s', request.get_data())

#-------------------------@
# Ruta principal del chatbot
@app.route('/')
def chatbot():
    if 'username' not in session: return redirect('/login')

    return render_template('aede.html')

#+++++++++++++++++++++++++++++++++++++++
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Datos de usuarios (solo para ejemplo)
    users = {
        'javier':  'surdelmundo',
        'nicolas': 'pepelon',
        'julio':   'boss'
    }
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            logging.info("Login usuario "+ username )
            session['username'] = username
            return redirect('/')
        else:
            logging.info("Bad login usuario "+ username )
            return 'Usuario o contraseña incorrectos.'

    return render_template('login.html')

#+++++++++++++++++++++++++++++++++++++++
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

#-------------------------@
# reset de la conversacion
@app.route('/reset', methods=['POST'])
def reset_conversacion():
    if 'username' not in session: return redirect('/login')
    global conversacion

    conversacion = inicia_chat()
    return redirect('/')

#-------------------------@
# Ruta API REST para recibir y procesar las solicitudes del usuario
@app.route('/chat', methods=['POST'])
def procesar_mensaje():
    if 'username' not in session: return redirect('/login')
    global contexto

    mensaje_usuario = request.json['user_input'] + ". Recuerda deducir fecha y el JSON al final."

    logging.info("Usuario: "+ session["username"]+ "/ Pregunta: "+ mensaje_usuario)

    ( respuesta_chatbot, entities ) = obtener_respuesta_chatbot(mensaje_usuario)

    logging.info("Usuario: "+ session["username"]+ "/ Respuesta: "+ respuesta_chatbot)

    respuesta_sin_JSON = cortar_string(respuesta_chatbot,"JSON")

    response = { 'message': respuesta_sin_JSON, 'entities': entities }
    return jsonify(response)

#----------------------------------------------------------------
# Función para obtener la respuesta del chatbot utilizando OpenAI
# esta no es una ruta, sino una funcion 
def obtener_respuesta_chatbot(mensaje_usuario):
    global conversacion

    mensaje = mensaje_usuario

    conversacion.append({"role": "user", "content": mensaje})

    # Obtener la respuesta del chatbot y actualizar el contexto de la conversación
    try:
      respuesta_chatbot = openai.ChatCompletion.create(
         messages = conversacion,
         model  = "gpt-3.5-turbo",
         max_tokens = 200,
         temperature = 0
      )["choices"][0]["message"]["content"]
    except openai.error.APIError as e:
        error_message = e.message
        status_code = e.status
        error_code = e.code
        response_body = e.response.body
        return "Prueba de nuevo: " + error_messaje
    except Exception as e:
        return "Error: " + e.__str__()

    #wf.escribir_en_archivo_csv([], mensaje_usuario, respuesta_chatbot, imc, pc_mas_cercano, "ail_preguntas.csv")

    conversacion.append({"role": "assistant", "content": respuesta_chatbot})

    entities = detect_entities(respuesta_chatbot)

    # Retornar la respuesta del chatbot al usuario
    return respuesta_chatbot, entities

def detect_entities(respuesta_IA):
    # Aquí debes implementar la lógica para detectar las entidades
    # y generar el diccionario de código-valor
    # Puedes utilizar bibliotecas de procesamiento de lenguaje natural 
    # como Spacy o NLTK

    # Ejemplo de entidades detectadas
    
    entities = encontrar_json(respuesta_IA)

    return entities

def encontrar_json(cadena):
    # Buscar el inicio y fin del JSON dentro de la cadena
    inicio = cadena.find('{')
    fin = cadena.find('}', inicio) + 1
    
    if inicio == -1 or fin == 0:
        # No se encontró un JSON válido
        return None
    
    json_str = cadena[inicio:fin]
    logging.info("json str: " + json_str )
    
    try:
        # Analizar el JSON y devolver el objeto resultante como un diccionario
        json_dict = json.loads(json_str)
        logging.info(json_dict )
        return json_dict
    except json.JSONDecodeError:
        # El JSON no es válido
        return None

def cortar_string(string, palabra):
    partes = string.split(palabra, 1)  # Dividir solo en la primera ocurrencia
    return partes[0]

if __name__ == '__main__':
    # Configurar el controlador de archivo
    #file_handler = logging.FileHandler('ail.log')
    #file_handler.setLevel(logging.INFO)
    #file_handler.setFormatter(formatter)  # Asignar el formateador personalizado al controlador de archivo

    # Agregar el controlador de archivo al registro
    #app.logger.addHandler(file_handler)

    app.run()


