import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# URL de la página web
url = 'http://34.145.131.242:5000'

# Datos de inicio de sesión
username = 'nicolas'
password = 'pepelon'

# Configurar opciones para manejar caracteres compuestos
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-features=VizDisplayCompositor')
options.add_argument('--lang=en_US.UTF-8')

# Iniciar sesión y obtener el controlador del navegador
driver = webdriver.Chrome(options=options)  # Requiere tener Chrome WebDriver instalado y en el PATH
driver.get(url + '/login')

try:
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button.click()
except NoSuchElementException:
    print('Error: No se encontraron los campos de inicio de sesión')
    driver.quit()
    exit(1)
except ElementNotInteractableException:
    print('Error: No se puede interactuar con los campos de inicio de sesión')
    driver.quit()
    exit(1)

# Leer las preguntas desde el archivo preguntas.txt
preguntas = []
with open('preguntas.txt', 'r', encoding='utf-8') as file:
    preguntas = [line.strip() for line in file]

# Abrir el archivo de salida respuestas.csv
with open('respuestas.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Pregunta', 'Respuesta'])  # Escribir encabezados de columna

    # Realizar las preguntas y escribir las respuestas en el archivo
    for i, pregunta in enumerate(preguntas, start=1):
        print(f'Realizando pregunta {i}: {pregunta}')

        try:
            # Escribir la pregunta en el campo de texto
            input_box = driver.find_element(By.ID, 'inputbox')
            input_box.clear()
            input_box.send_keys(pregunta)

            # Hacer clic en el botón de enviar
            preguntar_button = driver.find_element(By.XPATH, '//input[@value="Preguntar"]')
            preguntar_button.click()

            # Esperar un breve tiempo para que la respuesta aparezca en la página
            time.sleep(10)

            # Obtener la respuesta del elemento <p> con la clase "asistente"
            #respuesta_tag = driver.find_element(By.XPATH, '//p[@class="asistente"]')
            #respuesta_tag = driver.find_element(By.XPATH, '//p[@class="asistente"]')
			# Obtener la respuesta del último elemento <p> con la clase "asistente"
            respuesta_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//p[@class="asistente"]'))
            )[-1]
            respuesta = respuesta_tag.text.strip()
            #respuesta = respuesta_tag.text.strip()

            # Escribir la pregunta y la respuesta en el archivo
            writer.writerow([pregunta, respuesta])

            # Reiniciar la conversación después de 3 preguntas
            if i % 3 == 0:
                reset_button = driver.find_element(By.XPATH, '//input[@value="Reinicie la conversación"]')
                reset_button.click()

        except NoSuchElementException:
            print(f'Error: No se encontró un elemento en la pregunta {i}')
        except ElementNotInteractableException:
            print(f'Error: No se puede interactuar con un elemento en la pregunta {i}')

# Cerrar el navegador
driver.quit()

print('¡Prueba finalizada! Las respuestas se han guardado en respuestas.csv.')
