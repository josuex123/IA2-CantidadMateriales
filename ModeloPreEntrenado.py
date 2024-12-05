import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3

# Configuración del motor de texto a voz
def hablar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

# Función para reconocimiento de voz
def reconocer_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("¿Qué tipo de construcción necesitas? Di: 'loza', 'cimentación' o 'columnas' y la cantidad.")
        hablar("¿Qué tipo de construcción necesitas? Di: loza, cimentación o columnas y la cantidad.")
        try:
            audio = recognizer.listen(source)
            comando = recognizer.recognize_google(audio, language="es-ES")
            print(f"Escuché: {comando}")
            return comando
        except sr.UnknownValueError:
            print("No entendí lo que dijiste. Intenta nuevamente.")
            hablar("No entendí lo que dijiste. Intenta nuevamente.")
            return None
        except sr.RequestError:
            print("Hubo un error con el servicio de reconocimiento de voz.")
            hablar("Hubo un error con el servicio de reconocimiento de voz.")
            return None

# Función para calcular los materiales
def calcular_materiales(tipo, cantidad):
    if tipo == "loza":
        cemento_por_m2 = 7
        arena_por_m2 = 0.07
        grava_por_m2 = 0.07
        agua_por_m2 = 20
    elif tipo == "cimentación":
        cemento_por_m3 = 9.3
        arena_por_m3 = 0.45
        grava_por_m3 = 0.65
        agua_por_m3 = 190
    elif tipo == "columnas":
        cemento_por_m3 = 10.5
        arena_por_m3 = 0.38
        grava_por_m3 = 0.85
        agua_por_m3 = 200
    else:
        return None

    if tipo == "loza":
        cemento_total = cemento_por_m2 * cantidad
        arena_total = arena_por_m2 * cantidad
        grava_total = grava_por_m2 * cantidad
        agua_total = agua_por_m2 * cantidad
    else:
        cemento_total = cemento_por_m3 * cantidad
        arena_total = arena_por_m3 * cantidad
        grava_total = grava_por_m3 * cantidad
        agua_total = agua_por_m3 * cantidad

    return cemento_total, arena_total, grava_total, agua_total

# Función principal para manejar el comando de voz y calcular materiales
def procesar_comando():
    comando = reconocer_voz()
    if comando:
        try:
            palabras = comando.lower().split()
            tipo = None
            cantidad = None

            # Buscar el tipo de construcción
            if "loza" in palabras:
                tipo = "loza"
            elif "cimentación" in palabras:
                tipo = "cimentación"
            elif "columna" in palabras or "columnas" in palabras:
                tipo = "columnas"

            # Buscar la cantidad
            for palabra in palabras:
                palabra_limpia = ''.join(c for c in palabra if c.isdigit())
                if palabra_limpia.isdigit():
                    cantidad = int(palabra_limpia)
                    break

            if tipo and cantidad:
                cemento, arena, grava, agua = calcular_materiales(tipo, cantidad)
                respuesta = (
                    f"Para {cantidad} metros de {tipo}, necesitas: \n"
                    f"{cemento} bolsas de cemento,\n {arena:.2f} metros cúbicos de arena,\n "
                    f"{grava:.2f} metros cúbicos de grava, y \n{agua:.2f} litros de agua."
                )
                hablar(respuesta)
                return respuesta
            else:
                respuesta = "No entendí el tipo de construcción o la cantidad."
                hablar(respuesta)
                return respuesta
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            hablar("Ocurrió un error al procesar tu solicitud.")
            return "Ocurrió un error al procesar tu solicitud."

class Aplicacion:
    def __init__(self, master):
        self.master = master
        self.master.title("Reconocimiento de Voz - Cálculo de Materiales")
        self.master.geometry("500x400")

        self.boton_grabar = tk.Button(self.master, text="Grabar Comando", command=self.grabar_comando, width=20)
        self.boton_grabar.pack(pady=20)

        self.texto_resultado = tk.Label(self.master, text="Resultado aparecerá aquí", justify="left", width=50, height=10, anchor="nw")
        self.texto_resultado.pack(pady=20)

    def grabar_comando(self):
        resultado = procesar_comando()  
        self.texto_resultado.config(text=resultado)  

# Iniciar la interfaz gráfica
root = tk.Tk()
app = Aplicacion(root)
root.mainloop()
