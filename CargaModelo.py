from ModeloEntrenado import ModeloReconocimiento

def predecir_audio(audio_path):
    """
    Carga el modelo y predice la categoría de un archivo de audio.
    """
    modelo = ModeloReconocimiento()
    modelo.cargar_modelo()
    categoria = modelo.predecir(audio_path)
    print(f"La categoría predicha es: {categoria}")
    return categoria

if __name__ == "__main__":
    # Prueba con un archivo de audio
    audio_prueba = "dataset/comandoColu.wav"  # Cambia esta ruta por tu archivo de prueba
    predecir_audio(audio_prueba)
