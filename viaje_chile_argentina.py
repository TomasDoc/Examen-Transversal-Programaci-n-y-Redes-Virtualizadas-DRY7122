# viaje_chile_argentina.py

import requests

# === Configura tu API key de GraphHopper ===
API_KEY = "02297564-94da-42b9-8f69-1bbc572c0911"  # Reemplaza esto con tu clave personal de GraphHopper

def obtener_ruta(origen, destino, medio_transporte):
    url = f"https://graphhopper.com/api/1/route?key={API_KEY}"
    params = {
        "point": [origen, destino],
        "vehicle": medio_transporte,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        info = data['paths'][0]
        distancia_km = round(info['distance'] / 1000, 2)
        distancia_millas = round(distancia_km * 0.621371, 2)
        duracion_min = round(info['time'] / 1000 / 60, 2)
        narrativa = info['instructions']

        print(f"\nDistancia: {distancia_km} km ({distancia_millas} millas)")
        print(f"Duración estimada: {duracion_min} minutos")
        print("\nNarrativa del viaje:")
        for paso in narrativa:
            print("-", paso['text'])
        print()
    else:
        print("Error al obtener datos. Verifica las ciudades o tu API key.")

def main():
    print("=== Calculadora de Ruta Chile – Argentina ===")

    while True:
        origen = input("Ingrese ciudad de origen (o 's' para salir): ")
        if origen.lower() == 's':
            break

        destino = input("Ingrese ciudad de destino (o 's' para salir): ")
        if destino.lower() == 's':
            break

        print("\nSeleccione medio de transporte:")
        print("1. auto")
        print("2. bicicleta")
        print("3. a pie")
        tipo = input("Opción (1/2/3): ")

        vehiculos = {'1': 'car', '2': 'bike', '3': 'foot'}
        medio = vehiculos.get(tipo, 'car')

        obtener_ruta(origen, destino, medio)

if __name__ == "__main__":
    main()
