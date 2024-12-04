import os
import librosa
import numpy as np
import pickle
from sklearn.mixture import GaussianMixture

# Ruta del dataset
DATASET_DIR = "dataset"
MODELO_DIR = "modelos"

def extraer_caracteristicas(audio_path):
    """
    Extrae las características de MFCC de un archivo de audio.
    """
    y, sr = librosa.load(audio_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

def entrenar_modelo():
    """
    Entrena un modelo HMM-GMM con los audios en el dataset.
    """
    modelos = {}

    # Iterar sobre las categorías en el directorio dataset
    for categoria in os.listdir(DATASET_DIR):
        categoria_path = os.path.join(DATASET_DIR, categoria)
        
        # Verificar si es una carpeta (categoría)
        if os.path.isdir(categoria_path):
            print(f"Entrenando para la categoría: {categoria}")
            caracteristicas = []

            # Iterar sobre los archivos dentro de la categoría
            for archivo in os.listdir(categoria_path):
                archivo_path = os.path.join(categoria_path, archivo)
                
                # Solo procesar archivos .wav
                if archivo.endswith(".wav"):
                    try:
                        # Extraer características
                        mfcc = extraer_caracteristicas(archivo_path)
                        caracteristicas.append(mfcc)
                    except Exception as e:
                        print(f"Error procesando {archivo}: {e}")

            # Entrenar un modelo GMM
            gmm = GaussianMixture(n_components=4, covariance_type='diag', max_iter=200)
            gmm.fit(caracteristicas)
            modelos[categoria] = gmm

    # Guardar los modelos entrenados
    if not os.path.exists(MODELO_DIR):
        os.makedirs(MODELO_DIR)

    with open(os.path.join(MODELO_DIR, "modelo_gmm.pkl"), "wb") as f:
        pickle.dump(modelos, f)

    print("Entrenamiento completo. Modelos guardados en 'modelos/'.")

if __name__ == "__main__":
    entrenar_modelo()
