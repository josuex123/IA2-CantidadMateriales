import pickle
import librosa
import numpy as np

MODELO_PATH = "modelos/modelo_hmm_gmm.pkl"


def extraer_caracteristicas(audio_path):
    """
    Extrae las características MFCC de un archivo de audio.
    """
    try:
        y, sr = librosa.load(audio_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfcc.T, axis=0)
    except Exception as e:
        print(f"Error al procesar el archivo {audio_path}: {e}")
        return None


class ModeloReconocimiento:
    def __init__(self):
        self.modelos = None

    def cargar_modelo(self):
        """
        Carga el modelo HMM-GMM entrenado desde el archivo.
        """
        try:
            with open(MODELO_PATH, "rb") as f:
                self.modelos = pickle.load(f)
        except FileNotFoundError:
            raise ValueError(f"No se encontró el modelo en la ruta: {MODELO_PATH}")

    def predecir(self, audio_path):
        """
        Realiza la predicción con el modelo cargado.
        """
        if self.modelos is None:
            raise ValueError("El modelo no ha sido cargado. Usa 'cargar_modelo()'.")

        caracteristicas = extraer_caracteristicas(audio_path)
        if caracteristicas is None:
            raise ValueError("No se pudieron extraer características del audio.")

        max_puntaje = float("-inf")
        mejor_categoria = None

        for categoria, modelo in self.modelos.items():
            try:
                # Evaluar la puntuación del modelo HMM para las características extraídas
                puntaje = modelo.score([caracteristicas])
                if puntaje > max_puntaje:
                    max_puntaje = puntaje
                    mejor_categoria = categoria
            except Exception as e:
                print(f"Error al predecir para la categoría '{categoria}': {e}")

        return mejor_categoria


if __name__ == "__main__":
    modelo_reconocimiento = ModeloReconocimiento()
    modelo_reconocimiento.cargar_modelo()

    audio_prueba = "ruta/del/audio_prueba.wav"
    resultado = modelo_reconocimiento.predecir(audio_prueba)

    if resultado:
        print(f"El audio pertenece a la categoría: {resultado}")
    else:
        print("No se pudo clasificar el audio.")
