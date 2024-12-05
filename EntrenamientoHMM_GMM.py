import os
import librosa
import numpy as np
import pickle
from hmmlearn import hmm
from sklearn.preprocessing import StandardScaler

# Ruta del dataset y modelos
DATASET_DIR = "dataset"
MODELO_DIR = "modelos"

def extraer_caracteristicas(audio_path):
    """
    Extrae características MFCC de un archivo de audio.
    """
    try:
        # Cargar el archivo de audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Extraer MFCCs y calcular la media a lo largo del tiempo
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc = np.mean(mfcc.T, axis=0)
        
        return mfcc
    except Exception as e:
        print(f"Error al procesar el archivo {audio_path}: {e}")
        return None

def entrenar_modelo_hmm_gmm():
    """
    Entrena un modelo HMM-GMM con los audios en el dataset.
    """
    modelos = {}
    scaler = StandardScaler()  # Escalador para normalizar las características

    # Iterar sobre las categorías en el directorio dataset
    for categoria in os.listdir(DATASET_DIR):
        categoria_path = os.path.join(DATASET_DIR, categoria)
        
        if os.path.isdir(categoria_path):
            print(f"Entrenando para la categoría: {categoria}")
            caracteristicas = []

            # Procesar cada archivo .wav en la categoría
            for archivo in os.listdir(categoria_path):
                archivo_path = os.path.join(categoria_path, archivo)
                
                if archivo.endswith(".wav"):
                    mfcc = extraer_caracteristicas(archivo_path)
                    if mfcc is not None:
                        caracteristicas.append(mfcc)

            if not caracteristicas:
                print(f"No se encontraron características válidas para la categoría {categoria}.")
                continue

            # Convertir las características en una matriz numpy
            caracteristicas = np.array(caracteristicas)

            # Normalizar las características
            caracteristicas = scaler.fit_transform(caracteristicas)

            # Configurar y entrenar el modelo HMM
            num_estados = 4  # Ajustar según la complejidad de los datos
            hmm_model = hmm.GaussianHMM(
                n_components=num_estados,
                covariance_type='diag',
                n_iter=500,  # Incrementar iteraciones para mejorar convergencia
                tol=1e-4
            )

            try:
                hmm_model.fit(caracteristicas)
                modelos[categoria] = hmm_model
                print(f"Modelo para la categoría '{categoria}' entrenado correctamente.")
            except Exception as e:
                print(f"Error entrenando el modelo para la categoría {categoria}: {e}")

    # Crear directorio para guardar los modelos si no existe
    if not os.path.exists(MODELO_DIR):
        os.makedirs(MODELO_DIR)

    # Guardar los modelos entrenados en un archivo .pkl
    with open(os.path.join(MODELO_DIR, "modelo_hmm_gmm.pkl"), "wb") as f:
        pickle.dump(modelos, f)

    print("Entrenamiento completo. Modelos guardados en 'modelos/'.")

if __name__ == "__main__":
    entrenar_modelo_hmm_gmm()
