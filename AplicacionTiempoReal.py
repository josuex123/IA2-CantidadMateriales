import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
from scipy.io.wavfile import write
from ModeloEntrenadoHMM_GMM import ModeloReconocimiento

DURACION = 5  
FRECUENCIA_MUESTREO = 44100  

def grabar_audio_en_tiempo_real(nombre_archivo="dataset/comando.wav"):
    """
    Graba audio desde el micrófono y guarda en un archivo .wav.
    """
    print("Grabando... Habla ahora!")
    grabacion = sd.rec(int(DURACION * FRECUENCIA_MUESTREO), samplerate=FRECUENCIA_MUESTREO, channels=1, dtype='int16')
    sd.wait()  # Esperar a que termine la grabación
    write(nombre_archivo, FRECUENCIA_MUESTREO, grabacion)  # Guardar la grabación
    print(f"Grabación completa: {nombre_archivo}")
    return nombre_archivo

def convertir_audio_a_texto_con_modelo(archivo_audio):
    """
    Convierte un archivo de audio en texto usando el modelo entrenado.
    """
    # Inicializar y cargar el modelo
    modelo = ModeloReconocimiento()
    modelo.cargar_modelo()

    # Utilizamos el modelo entrenado para hacer la predicción del comando
    texto = modelo.predecir(archivo_audio)  # Se asume que 'predecir' es el método para hacer predicciones con el modelo
    return texto

def calcular_materiales(tipo, cantidad):
    if tipo == "loza":
        cemento_por_m2 = 7  # en bolsas de 46kg
        arena_por_m2 = 0.07  # en metros cúbicos
        grava_por_m2 = 0.07  # en metros cúbicos
        agua_por_m2 = 20  # en litros
    elif tipo == "cimentación":
        cemento_por_m3 = 9.3  # en bolsas de 46kg
        arena_por_m3 = 0.45  # en metros cúbicos
        grava_por_m3 = 0.65  # en metros cúbicos
        agua_por_m3 = 190  # en litros
    elif tipo == "columnas":
        cemento_por_m3 = 10.5  # en bolsas de 46kg
        arena_por_m3 = 0.38  # en metros cúbicos
        grava_por_m3 = 0.85  # en metros cúbicos
        agua_por_m3 = 200  # en litros
    else:
        return None

    if tipo == "loza":
        cemento = cemento_por_m2 * cantidad
        arena = arena_por_m2 * cantidad
        grava = grava_por_m2 * cantidad
        agua = agua_por_m2 * cantidad
    else:
        cemento = cemento_por_m3 * cantidad
        arena = arena_por_m3 * cantidad
        grava = grava_por_m3 * cantidad
        agua = agua_por_m3 * cantidad

    return cemento, arena, grava, agua

def predecir_comando_en_tiempo_real():
    """
    Predice la categoría y la cantidad de un comando hablado en tiempo real usando el modelo entrenado.
    """
    # Grabar audio desde el micrófono
    archivo_audio = grabar_audio_en_tiempo_real()

    # Convertir el audio grabado a texto usando el modelo entrenado
    texto = convertir_audio_a_texto_con_modelo(archivo_audio)

    if texto:
        # Dividir el texto en palabras
        palabras = texto.lower().split()
        
        # Identificar la categoría (por ejemplo, "loza", "columnas", "cimentacion")
        tipo = None
        for palabra in palabras:
            if palabra in ["loza", "cimentacion", "columnas"]:
                tipo = palabra
                break
        
        # Extraer la cantidad (buscando un número en el texto)
        cantidad = None
        for palabra in palabras:
            if palabra.isdigit():
                cantidad = int(palabra)
                break
        
        # Verificar si se reconoció la categoría y cantidad
        if tipo and cantidad:
            materiales = calcular_materiales(tipo, cantidad)
            if materiales:
                cemento, arena, grava, agua = materiales
                return f"Para {cantidad} metros de {tipo} necesitas:\n- {cemento} bolsas de cemento\n- {arena:.2f} metros cúbicos de arena\n- {grava:.2f} metros cúbicos de grava\n- {agua:.2f} litros de agua"
            else:
                return "No se pudo calcular los materiales."
        else:
            return "No se pudo determinar el tipo o cantidad del comando."
    else:
        return "No se pudo reconocer el comando."

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
        resultado = predecir_comando_en_tiempo_real()
        self.texto_resultado.config(text=resultado)

root = tk.Tk()
app = Aplicacion(root)
root.mainloop()
