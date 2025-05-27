import discord
import requests
from .json_dbp import cargar_datos
import os
from dotenv import load_dotenv

load_dotenv()
CANAL_ID = int(os.getenv('CANAL_ID'))

async def status_task(bot):
    canal = bot.get_channel(CANAL_ID)
    if not canal:
        print("⚠️ No se encontró el canal.")
        return

    for guild in bot.guilds:
        servidor_id = str(guild.id)
        data = cargar_datos()

        if servidor_id not in data:
            continue

        erroneas = []

        for usuario_id, info in data[servidor_id].items():
            urls = info.get("urls", [])
            for u in urls:
                try:
                    response = requests.get(u, timeout=5)
                    
                except:
                    erroneas.append(f"<@{usuario_id}>\n{u} ")


        
        if erroneas:
            embed = discord.Embed(
                title="🔎 Revisión automática de URLs",
                description="**❌ URLs  caidas:**\n" + "\n".join(erroneas),
                color=discord.Color.red()  # borde rojo para errores
            )
        else:
            embed = discord.Embed(
                title="🔎 Revisión automática de URLs",
                description=f"✅ Todas las URLs están accesibles en **{guild.name}**.",
                color=discord.Color.green()
            )

        await canal.send(embed=embed)
