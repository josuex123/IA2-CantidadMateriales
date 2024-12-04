import os
from ModeloEntrenado import ModeloReconocimiento

def calcular_materiales(tipo, cantidad):
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

def main():
    modelo = ModeloReconocimiento()
    modelo.cargar_modelo()

    print("Habla la categoría de construcción y cantidad (por ejemplo: 'loza 10').")
    archivo_audio = "dataset/comandoColu.wav"  # Aquí debes grabar el comando de voz
    tipo = modelo.predecir(archivo_audio)

    if tipo:
        cantidad = 10  # Supón que extraes este valor del comando de voz
        materiales = calcular_materiales(tipo, cantidad)

        if materiales:
            cemento, arena, grava, agua = materiales
            print(
                f"Para {cantidad} metros de {tipo} necesitas: "
                f"{cemento} bolsas de cemento, {arena:.2f} metros cúbicos de arena, "
                f"{grava:.2f} metros cúbicos de grava y {agua:.2f} litros de agua."
            )
        else:
            print("No se pudo calcular los materiales.")
    else:
        print("No se pudo determinar el tipo de construcción.")

if __name__ == "__main__":
    main()
