from flask import Flask, render_template, request, redirect, session
import os, openai
import web_funciones as wf

def inicia_chat():
   chat = []  # Reinicia la variable de conversación
   mensaje = "Eres AIL, el Asistente de Información Legal de Consorcio. "
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

#-------------------------@
# Ruta principal del chatbot
@app.route('/')
def chatbot():
    if 'username' in session:
      return render_template('chatbot.html')
    else:
      return redirect('/login')

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
            session['username'] = username
            return redirect('/')
        else:
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
    global conversacion, primero
    conversacion = inicia_chat()
    primero = True
    return redirect('/')

#-------------------------@
# Ruta API REST para recibir y procesar las solicitudes del usuario
@app.route('/mensaje', methods=['POST'])
def procesar_mensaje():
    mensaje_usuario = request.form['mensaje']
    respuesta_chatbot = obtener_respuesta_chatbot(mensaje_usuario)
    return respuesta_chatbot

#----------------------------------------------------------------
# Función para obtener la respuesta del chatbot utilizando OpenAI
# esta no es una ruta, sino una funcion 
def obtener_respuesta_chatbot(mensaje_usuario):
    global conversacion
    global parrafos, archivos, textos, embeddings
    global primero

    if primero:
        vector = wf.read_embedding(mensaje_usuario)
        (contexto, imc, pc_mas_cercano) = wf.busca_contexto(vector, embeddings, textos)
        conversacion.append({"role": "user", "content": contexto})
        primero = False

    mensaje = "responde la pregunta solo con la informacion entregada: " + mensaje_usuario
    conversacion.append({"role": "user", "content": mensaje})

    # Obtener la respuesta del chatbot y actualizar el contexto de la conversación
    try:
      respuesta_chatbot = openai.ChatCompletion.create(
         messages = conversacion,
         model  = "gpt-3.5-turbo",
         max_tokens = 100,
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

    conversacion.append({"role": "assistant", "content": respuesta_chatbot})

    # Retornar la respuesta del chatbot al usuario
    return respuesta_chatbot

if __name__ == '__main__':
    app.run(debug=True)

