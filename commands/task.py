import discord
import requests
from .json_dbp import cargar_datos
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo 

load_dotenv()
CANAL_ID = int(os.getenv('CANAL_ID'))
MENSAJE_FILE = "mensaje_status.json"

hora_espana = datetime.now(ZoneInfo("Europe/Madrid"))
def guardar_mensaje_id(guild_id, channel_id, message_id):
    try:
        with open(MENSAJE_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[guild_id] = {"channel_id": channel_id, "message_id": message_id}

    with open(MENSAJE_FILE, "w") as f:
        json.dump(data, f)

def cargar_mensaje_id(guild_id):
    try:
        with open(MENSAJE_FILE, "r") as f:
            data = json.load(f)
            return data.get(guild_id)
    except FileNotFoundError:
        return None

async def status_task(bot):
    for guild in bot.guilds:
        servidor_id = str(guild.id)
        canal = bot.get_channel(CANAL_ID)
        if not canal:
            print("⚠️ No se encontró el canal.")
            return

        data = cargar_datos()

        if servidor_id not in data:
            continue

        resultado_urls = []

        for usuario_id, info in data[servidor_id].items():
            urls = info.get("urls", [])
            for u in urls:
                try:
                    response = requests.get(u, timeout=5)
                    if response.status_code == 200:
                       resultado_urls.append(f"<a:online:1376996976843030539> {u}")


                    else:
                        resultado_urls.append(f"<a:error2:1377008688052830399> <@{usuario_id}> {u} (Status: {response.status_code})")
                except:
                    resultado_urls.append(f"<a:error2:1377008688052830399> <@{usuario_id}> {u} (Sin respuesta)")
        
        embed = discord.Embed(
            title="🔎 Revisión automática de URLs",
            description="\n".join(resultado_urls) if resultado_urls else "No se encontraron URLs para revisar.",
            color=discord.Color.red() if any("<a:error2:1377008688052830399>" in r for r in resultado_urls) else discord.Color.blue(),
            

        )

        embed.set_footer(text=f"Last fetch: {hora_espana.strftime('%Y-%m-%d %H:%M:%S')} ")
            
        

        mensaje_info = cargar_mensaje_id(servidor_id)
        if mensaje_info:
            try:
                canal = bot.get_channel(int(mensaje_info["channel_id"]))
                mensaje = await canal.fetch_message(int(mensaje_info["message_id"]))
                await mensaje.edit(embed=embed)
                return
            except:
                pass

        mensaje = await canal.send(embed=embed)
        guardar_mensaje_id(servidor_id, canal.id, mensaje.id)
