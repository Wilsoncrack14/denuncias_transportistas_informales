import requests 
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

def validate_dni(dni):
    # MOCK FOR DEVELOPMENT: If no API key is set, return fake data
    if not API_KEY:
        return {
  "dni": "string",
  "nombres": "string",
  "apellidoPaterno": "string",
  "apellidoMaterno": "string",
  "codVerifica": "string"
}

    url = f"https://dniruc.apisperu.com/api/v1/dni/{dni}?token={API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return {"error": "Error al conectar con el servicio de validación de DNI."}
        return response.json()
    except Exception:
        return {"error": "Error de conexión"}