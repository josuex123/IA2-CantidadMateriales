import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import pickle
import numpy as np
import speech_recognition as sr
from ModeloEntrenado import ModeloReconocimiento

# Configuración de grabación
DURACION = 5  # Duración de la grabación en segundos
FRECUENCIA_MUESTREO = 44100  # Frecuencia de muestreo

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

def convertir_audio_a_texto(archivo_audio):
    """
    Convierte un archivo de audio en texto usando SpeechRecognition.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(archivo_audio) as fuente:
        audio = recognizer.record(fuente)  # Escuchar el archivo de audio

    try:
        # Usar el reconocedor de Google para convertir audio a texto
        texto = recognizer.recognize_google(audio)
        print(f"Texto reconocido: {texto}")
        return texto
    except sr.UnknownValueError:
        print("No se pudo reconocer el audio.")
        return None
    except sr.RequestError as e:
        print(f"Error con el servicio de reconocimiento de voz: {e}")
        return None

def calcular_materiales(tipo, cantidad):
    """
    Calcula los materiales necesarios para cada tipo de construcción.
    """
    if tipo == "loza":
        cemento = 7 * cantidad
        arena = 0.6 * cantidad
        grava = 0.6 * cantidad
        agua = 180 * cantidad
    elif tipo == "cimentacion":
        cemento = 8 * cantidad
        arena = 0.5 * cantidad
        grava = 0.8 * cantidad
        agua = 200 * cantidad
    elif tipo == "columnas":
        cemento = 10 * cantidad
        arena = 0.4 * cantidad
        grava = 0.9 * cantidad
        agua = 210 * cantidad
    else:
        return None

    return cemento, arena, grava, agua

def predecir_comando_en_tiempo_real():
    """
    Predice la categoría y la cantidad de un comando hablado en tiempo real.
    """
    # Inicializar y cargar el modelo
    modelo = ModeloReconocimiento()
    modelo.cargar_modelo()

    # Grabar audio desde el micrófono
    archivo_audio = grabar_audio_en_tiempo_real()

    # Convertir el audio grabado a texto
    texto = convertir_audio_a_texto(archivo_audio)

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
            print(f"Comando: {tipo} {cantidad}")
            materiales = calcular_materiales(tipo, cantidad)
            if materiales:
                cemento, arena, grava, agua = materiales
                print(f"Para {cantidad} metros de {tipo} necesitas:")
                print(f"- {cemento} bolsas de cemento")
                print(f"- {arena:.2f} metros cúbicos de arena")
                print(f"- {grava:.2f} metros cúbicos de grava")
                print(f"- {agua:.2f} litros de agua")
            else:
                print("No se pudo calcular los materiales.")
        else:
            print("No se pudo determinar el tipo o cantidad del comando.")
    else:
        print("No se pudo reconocer el comando.")

if __name__ == "__main__":
    predecir_comando_en_tiempo_real()
