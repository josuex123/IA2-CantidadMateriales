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
        # Proporciones para 1 metro cuadrado de loza
        cemento_por_m2 = 7  # en bolsas de 50kg
        arena_por_m2 = 0.6  # en metros cúbicos
        grava_por_m2 = 0.6  # en metros cúbicos
        agua_por_m2 = 180   # en litros
    elif tipo == "cimentación":
        # Proporciones para 1 metro cúbico de cimentación
        cemento_por_m3 = 8  # en bolsas de 50kg
        arena_por_m3 = 0.5  # en metros cúbicos
        grava_por_m3 = 0.8  # en metros cúbicos
        agua_por_m3 = 200   # en litros
    elif tipo == "columnas":
        # Proporciones para 1 metro cúbico de columnas
        cemento_por_m3 = 10  # en bolsas de 50kg
        arena_por_m3 = 0.4  # en metros cúbicos
        grava_por_m3 = 0.9  # en metros cúbicos
        agua_por_m3 = 210   # en litros
    else:
        return None

    # Cálculo total según el tipo
    if tipo == "loza":
        cemento_total = cemento_por_m2 * cantidad
        arena_total = arena_por_m2 * cantidad
        grava_total = grava_por_m2 * cantidad
        agua_total = agua_por_m2 * cantidad
    else:  # cimentación o columnas
        cemento_total = cemento_por_m3 * cantidad
        arena_total = arena_por_m3 * cantidad
        grava_total = grava_por_m3 * cantidad
        agua_total = agua_por_m3 * cantidad

    return cemento_total, arena_total, grava_total, agua_total

# Lógica principal
def main():
    comando = reconocer_voz()
    if comando:
        # Procesar el comando para extraer tipo y cantidad
        try:
            palabras = comando.split()
            tipo = None
            cantidad = None

            # Buscar el tipo de construcción
            if "loza" in palabras:
                tipo = "loza"
            elif "cimentación" in palabras:
                tipo = "cimentación"
            elif "columnas" in palabras:
                tipo = "columnas"

            # Buscar la cantidad (número)
            for palabra in palabras:
                if palabra.isdigit():
                    cantidad = int(palabra)
                    break

            if tipo and cantidad:
                cemento, arena, grava, agua = calcular_materiales(tipo, cantidad)
                respuesta = (
                    f"Para {cantidad} metros de {tipo}, necesitas: "
                    f"{cemento} bolsas de cemento, {arena:.2f} metros cúbicos de arena, "
                    f"{grava:.2f} metros cúbicos de grava, y {agua:.2f} litros de agua."
                )
                print(respuesta)
                hablar(respuesta)
            else:
                print("No entendí el tipo de construcción o la cantidad.")
                hablar("No entendí el tipo de construcción o la cantidad.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            hablar("Ocurrió un error al procesar tu solicitud.")

if __name__ == "__main__":
    main()
