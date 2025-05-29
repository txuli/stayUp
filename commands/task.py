import requests
import discord
from datetime import datetime
from zoneinfo import ZoneInfo
from db_queries import cargar_urls, cargar_mensaje_db, guardar_mensaje_db

async def status_task(bot):
    for guild in bot.guilds:
        servidor_id = guild.id
        urls = cargar_urls(servidor_id)

        if not urls:
            continue

        mensaje_info = cargar_mensaje_db(servidor_id)
        canal = None
        mensaje = None

        #  obtain the channel of the message
        if mensaje_info and mensaje_info["channel_id"]:
            canal = bot.get_channel(int(mensaje_info["channel_id"]))

        if not canal:
            print(f"⚠️ No se encontró el canal para el servidor {servidor_id}.")
            continue

        # verigfy each URL
        resultado_urls = []
       
        for item in urls:
            user_id = item.get("userId")
            mencion = f"<@{user_id}>" if user_id else ""
            url = item["url"]
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    resultado_urls.append(f"<a:online:1376996976843030539> {url}")
                else:
                    resultado_urls.append(f"<a:error2:1377008688052830399> {mencion} {url} (Status: {response.status_code}), ")
            except:
                resultado_urls.append(f"<a:error2:1377008688052830399> {mencion} {url} (Sin respuesta)")

        hora_espana = datetime.now(ZoneInfo("Europe/Madrid"))
        embed = discord.Embed(
            title="🔎 Revisión automática de URLs",
            description="\n".join(resultado_urls) if resultado_urls else "No se encontraron URLs para revisar.",
            color=discord.Color.red() if any("error2" in r for r in resultado_urls) else discord.Color.blue(),
        )
        embed.set_footer(text=f"Last fetch: {hora_espana.strftime('%Y-%m-%d %H:%M:%S')}")

        # try to edit the message
        if mensaje_info and mensaje_info["message_id"]:
            try:
                mensaje = await canal.fetch_message(int(mensaje_info["message_id"]))
                await mensaje.edit(embed=embed)
                continue  
            except:
                print(f"⚠️ No se pudo editar el mensaje en canal {canal.id}. Se enviará uno nuevo.")

       
        mensaje = await canal.send(embed=embed)
        guardar_mensaje_db(servidor_id, canal.id, mensaje.id)
