import pdb
import openai

# Establecer tu clave de API
openai.api_key = "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"

def completar_texto(prompt):
    # Llamar a la función "openai.Completion.create" para hacer la solicitud
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None
    )

    # Obtener la respuesta generada
    if response.choices:
        return response.choices[0].text.strip()
    else:
        return "No se recibió ninguna respuesta."

# Ejemplo de uso
prompt = "Una vez en un pueblo lejano"
pdb.set_trace()  # Establecer un punto de interrupción
texto_completado = completar_texto(prompt)
print(texto_completado)
