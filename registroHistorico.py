import sqlite3

class PreguntasFrecuentes:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS preguntas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            pregunta TEXT,
                            cantidad INTEGER DEFAULT 0
                        )''')
        self.conn.commit()

    def agregar_pregunta(self, pregunta):
        self.c.execute("SELECT * FROM preguntas WHERE pregunta=?", (pregunta,))
        registro = self.c.fetchone()
        if registro:
            self.c.execute("UPDATE preguntas SET cantidad=cantidad+1 WHERE id=?", (registro[0],))
        else:
            self.c.execute("INSERT INTO preguntas (pregunta) VALUES (?)", (pregunta,))
        self.conn.commit()

    def obtener_historico(self):
        self.c.execute("SELECT * FROM preguntas ORDER BY cantidad DESC")
        return self.c.fetchall()

    def cerrar_conexion(self):
        self.conn.close()


# Ejemplo de uso
if __name__ == "__main__":
    # Crear una instancia de la clase PreguntasFrecuentes
    preguntas_frecuentes = PreguntasFrecuentes("preguntas.db")

    # Registrar preguntas
    preguntas_frecuentes.agregar_pregunta("¿Cómo funciona Python?")
    preguntas_frecuentes.agregar_pregunta("¿Cuál es la sintaxis básica de Python?")
    preguntas_frecuentes.agregar_pregunta("¿Cómo puedo instalar paquetes en Python?")

    # Obtener el historico de preguntas
    historico = preguntas_frecuentes.obtener_historico()
    for pregunta in historico:
        print(f"Pregunta: {pregunta[1]} | Cantidad: {pregunta[2]}")

    # Cerrar la conexión a la base de datos
    preguntas_frecuentes.cerrar_conexion()
