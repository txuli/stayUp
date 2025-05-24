import json
import os

DATA_FILE = 'url.json'

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    
def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
def addUrl(url, servidor_id, usuario_id):
    
    data = cargar_datos()
    if servidor_id not in data:
        data[servidor_id] = {}
    if usuario_id not in data[servidor_id]:
        data[servidor_id][usuario_id] = {}
    if url not in data:
        data[url] = True
        guardar_datos(data)
        return True
    return False
