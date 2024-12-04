from CargaModelo import load_and_predict

def calculate_materials(area, tipo):
    """
    Calcula las cantidades de materiales necesarias para un área dada.
    """
    proporciones = {
        "loza": {"espesor": 0.1, "cemento": 300, "arena": 0.6, "grava": 0.8, "agua": 180},
        "cimentacion": {"espesor": 0.2, "cemento": 350, "arena": 0.5, "grava": 0.9, "agua": 200},
        "columna": {"espesor": 0.15, "cemento": 400, "arena": 0.4, "grava": 0.7, "agua": 190},
    }

    if tipo not in proporciones:
        raise ValueError(f"Tipo desconocido: {tipo}. Usa 'loza', 'cimentacion' o 'columna'.")

    datos = proporciones[tipo]
    volumen = area * datos["espesor"]  # Volumen en m³

    materiales = {
        "cemento": volumen * datos["cemento"],  # kg
        "arena": volumen * datos["arena"],      # m³
        "grava": volumen * datos["grava"],      # m³
        "agua": volumen * datos["agua"],        # litros
    }

    return materiales

if __name__ == "__main__":
    print("Aplicación de Reconocimiento de Voz para Construcción")
    model_path = "ModeloEntrenado.pkl"

    while True:
        print("\n1. Consultar proporciones")
        print("2. Calcular materiales")
        print("3. Salir")
        choice = input("Selecciona una opción: ")

        if choice == "1":
            audio_path = input("Graba tu pregunta y guarda el archivo .wav: ")
            prediction = load_and_predict(model_path, audio_path)
            print(f"Proporción para {prediction}:")
            if prediction == "loza":
                print("1 de cemento, 2 de arena, 4 de grava.")
            elif prediction == "cimentacion":
                print("1 de cemento, 3 de arena, 5 de grava.")
            elif prediction == "columna":
                print("1 de cemento, 2 de arena, 3 de grava.")
            else:
                print("Categoría no reconocida.")

        elif choice == "2":
            area = float(input("Ingresa el área en metros cuadrados: "))
            tipo = input("Ingresa el tipo de construcción (loza, cimentacion, columna): ").lower()
            try:
                materiales = calculate_materials(area, tipo)
                print("\nMateriales necesarios:")
                print(f"- Cemento: {materiales['cemento']:.2f} kg")
                print(f"- Arena: {materiales['arena']:.2f} m³")
                print(f"- Grava: {materiales['grava']:.2f} m³")
                print(f"- Agua: {materiales['agua']:.2f} litros")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            print("Saliendo de la aplicación. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")
