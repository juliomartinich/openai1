from flask import Flask, render_template, request, redirect, session, jsonify
import os, openai, logging, datetime, traceback
import web_funciones as wf

def inicia_chat():
   chat = []  # Reinicia la variable de conversación
   mensaje = "Eres AIL, el Asistente de Información Legal de Consorcio y yo soy un Cajero. "
   mensaje += "Responde basado solo en la informacion que yo te entregue. "
   mensaje += "Si la pregunta no se refiere a esa informacion responde No tengo informacion."
   chat.append({"role": "user", "content": mensaje})
   return chat

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')
app.secret_key = openai.api_key  # API openai de clave secreta para la sesión

(parrafos, archivos, textos, embeddings) = wf.read_stored_embeddings('mis_word_embed.csv')

# Variable global para mantener el contexto de la conversación
conversacion = inicia_chat()
mensaje = "aca te entrego informacion: " + textos[0]
conversacion.append({"role": "user", "content": mensaje})
primero = True

#configura logging
logging.basicConfig(filename='ail.log', level=logging.INFO)

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

    return render_template('chatbot.html')

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
    global conversacion, primero

    conversacion = inicia_chat()
    primero = True
    return redirect('/')

#-------------------------@
# Ruta API REST para recibir y procesar las solicitudes del usuario
@app.route('/mensaje', methods=['POST'])
def procesar_mensaje():
    if 'username' not in session: return redirect('/login')
    global contexto, imc, pc_mas_cercano

    mensaje_usuario = request.form['mensaje']

    logging.info("Usuario: "+ session["username"]+ "/ Pregunta: "+ mensaje_usuario)

    respuesta_chatbot = obtener_respuesta_chatbot(mensaje_usuario)
    respuesta = { 'mensaje': respuesta_chatbot, 'pc_mas_cercano': pc_mas_cercano }
    respuesta['contexto'] = contexto
    respuesta['imc'] = imc
    # ahora devuelvo un json
    return respuesta

#----------------------------------------------------------------
# Función para obtener la respuesta del chatbot utilizando OpenAI
# esta no es una ruta, sino una funcion 
def obtener_respuesta_chatbot(mensaje_usuario):
    global conversacion
    global parrafos, archivos, textos, embeddings
    global primero, contexto, imc, pc_mas_cercano

    if primero:
        pregunta = "¿ " + mensaje_usuario + " ?"
        vector = wf.read_embedding(pregunta)
        (contexto, imc, pc_mas_cercano) = wf.busca_contexto(vector, embeddings, textos)
        conversacion.append({"role": "user", "content": contexto})
        primero = False

    mensaje = "responde la pregunta solo con la informacion entregada en no mas de 100 palabras: ¿ "
    mensaje += wf.eliminar_signos_especiales(mensaje_usuario) + " ? "
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

    wf.escribir_en_archivo_csv([], mensaje_usuario, respuesta_chatbot, imc, pc_mas_cercano, "ail_preguntas.csv")

    conversacion.append({"role": "assistant", "content": respuesta_chatbot})

    # Retornar la respuesta del chatbot al usuario
    return respuesta_chatbot

if __name__ == '__main__':
    # Configurar el controlador de archivo
    #file_handler = logging.FileHandler('ail.log')
    #file_handler.setLevel(logging.INFO)
    #file_handler.setFormatter(formatter)  # Asignar el formateador personalizado al controlador de archivo

    # Agregar el controlador de archivo al registro
    #app.logger.addHandler(file_handler)

    app.run()


