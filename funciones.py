import os
import requests
import getpass
import argparse
import csv


def leer_apikey(path="apikey.txt"):
    if not os.path.exists(path):
        clave = getpass.getpass("Ingresa tu API key: ")
        with open(path, "w") as archivo:
            archivo.write(clave.strip())
    with open(path, "r") as archivo:
        return archivo.read().strip()


def obtener_argumentos():
    parser = argparse.ArgumentParser(
            description="Verifica un correo usando la API de HaveIBeenPwned.")
    parser.add_argument("correo", help="Correo electrónico a verificar")
    parser.add_argument("-o", "--output", default="reporte.csv",
                        help="Nombre del archivo CSV desalida")
    return parser.parse_args()


def consultar_brechas(correo, api_key):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}"
    headers = {"hibp-api-key": api_key, "user-agent": "PythonScript"}
    return requests.get(url, headers=headers)


def consultar_detalle(nombre, api_key):
    url = f"https://haveibeenpwned.com/api/v3/breach/{nombre}"
    headers = {"hibp-api-key": api_key, "user-agent": "PythonScript"}
    return requests.get(url, headers=headers)


def generar_csv(nombre_archivo, lista_detalles):
    with open(nombre_archivo, "w", newline='',
              encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["Título", "Dominio", "Fecha de Brecha",
                         "Datos Comprometidos", "Verificada", "Sensible"])
        for detalle in lista_detalles:
            writer.writerow([
                detalle.get("Title"),
                detalle.get("Domain"),
                detalle.get("BreachDate"),
                ", ".join(detalle.get("DataClasses", [])),
                "Sí" if detalle.get("IsVerified") else "No",
                "Sí" if detalle.get("IsSensitive") else "No"
            ])
