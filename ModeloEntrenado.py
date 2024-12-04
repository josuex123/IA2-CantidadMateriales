import pickle
import librosa
import numpy as np

MODELO_PATH = "modelos/modelo_gmm.pkl"

def extraer_caracteristicas(audio_path):
    """
    Extrae las características MFCC de un archivo de audio.
    """
    y, sr = librosa.load(audio_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

class ModeloReconocimiento:
    def __init__(self):
        self.modelos = None

    def cargar_modelo(self):
        """
        Carga el modelo GMM entrenado desde el archivo.
        """
        with open(MODELO_PATH, "rb") as f:
            self.modelos = pickle.load(f)

    def predecir(self, audio_path):
        """
        Realiza la predicción con el modelo cargado.
        """
        if self.modelos is None:
            raise ValueError("El modelo no ha sido cargado. Usa 'cargar_modelo()'.")

        caracteristicas = extraer_caracteristicas(audio_path)
        max_puntaje = float("-inf")
        mejor_categoria = None

        for categoria, modelo in self.modelos.items():
            puntaje = modelo.score([caracteristicas])
            if puntaje > max_puntaje:
                max_puntaje = puntaje
                mejor_categoria = categoria

        return mejor_categoria
