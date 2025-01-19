import requests
import base64
import os
import json
import time
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

API_KEY = os.getenv("API_KEY")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if not API_KEY or not CLIENT_SECRET:
    raise Exception("API_KEY o CLIENT_SECRET no definidos en el archivo .env")

DATA_FOLDER = os.path.join(os.getcwd(), "data_api_idealista")
os.makedirs(DATA_FOLDER, exist_ok=True)

MAX_REQUESTS = 100  # Límite de solicitudes por mes
REQUEST_DELAY = 1   # Retraso entre solicitudes (segundos)


class IdealistaAPI:
    def __init__(self, api_key, client_secret, max_requests=MAX_REQUESTS):
        self.api_key = api_key
        self.client_secret = client_secret
        self.max_requests = max_requests
        self.request_count = 0
        self.access_token = None

    def get_token(self):
        """Obtiene un token OAuth2 de la API Idealista."""
        url = "https://api.idealista.com/oauth/token"
        credentials = f"{self.api_key}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url, headers=headers, data={"grant_type": "client_credentials"})
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            print("Token obtenido correctamente.")
            return True
        else:
            print(f"Error obteniendo el token: {response.status_code}")
            print(response.text)
            return False

    def search_properties(self, location, distance, max_items=50, num_page=1):
        """Busca propiedades en una ubicación específica."""
        if self.request_count >= self.max_requests:
            print("Límite mensual de solicitudes alcanzado.")
            return None

        url = "https://api.idealista.com/3.5/es/search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        params = {
            "operation": "sale",
            "propertyType": "homes",
            "center": location,
            "distance": distance,
            "maxItems": max_items,
            "numPage": num_page,
        }

        print(f"Enviando solicitud #{self.request_count + 1}...")
        response = requests.post(url, headers=headers, data=params)
        time.sleep(REQUEST_DELAY)

        if response.status_code == 200:
            self.request_count += 1
            return response.json()
        else:
            print(f"Error obteniendo propiedades: {response.status_code}")
            print(response.text)
            return None


def generate_grid(center_lat, center_lon, radius, step_size):
    """Genera una cuadrícula de coordenadas alrededor de un punto central."""
    lat_steps = int(radius / step_size)
    lon_steps = int(radius / step_size)
    grid = []

    for i in range(-lat_steps, lat_steps + 1):
        for j in range(-lon_steps, lon_steps + 1):
            new_lat = center_lat + i * step_size
            new_lon = center_lon + j * step_size
            grid.append(f"{new_lat},{new_lon}")

    return grid


def main():
    api = IdealistaAPI(API_KEY, CLIENT_SECRET)
    if not api.get_token():
        return

    # Coordenadas centrales de Madrid
    madrid_center_lat = 40.4168
    madrid_center_lon = -3.7038
    radius = 5000  # Radio en metros
    step_size = 0.005  # Ajuste fino para cubrir áreas más pequeñas (~500 m)

    locations = generate_grid(madrid_center_lat, madrid_center_lon, radius, step_size)
    all_properties = []

    for location in locations:
        for page in range(1, 11):  # Hasta 10 páginas por ubicación
            data = api.search_properties(location, distance=500, num_page=page)
            if data and "elementList" in data:
                all_properties.extend(data["elementList"])
            else:
                break
            if api.request_count >= MAX_REQUESTS:
                print("Límite de solicitudes alcanzado.")
                break
        if api.request_count >= MAX_REQUESTS:
            break

    # Guardar datos obtenidos
    output_file = os.path.join(DATA_FOLDER, "madrid_properties_maximized.json")
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_properties, file, indent=4)
    print(f"Datos guardados en: {output_file}")

    print(f"Total de propiedades obtenidas: {len(all_properties)}")


if __name__ == "__main__":
    main()
