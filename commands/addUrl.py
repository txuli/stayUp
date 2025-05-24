import json
import os
import discord
from discord.ext import commands
from discord import app_commands

DATA_FILE = 'url.json'

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Comando slash definido fuera del Cog
@app_commands.command(name="addurl", description="Añade una URL al servidor")
async def addurl(interaction: discord.Interaction, url: str):
    print(f"📥 /addurl ejecutado por {interaction.user} con URL: {url}")
    servidor_id = str(interaction.guild_id)
    usuario_id = str(interaction.user.id)
    data = cargar_datos()

    if servidor_id not in data:
        data[servidor_id] = {}

    if usuario_id not in data[servidor_id]:
        data[servidor_id][usuario_id] = {"urls": []}

    if url in data[servidor_id][usuario_id]["urls"]:
        await interaction.response.send_message("⚠️ Esa URL ya está registrada.", ephemeral=True)
        return

    data[servidor_id][usuario_id]["urls"].append(url)
    guardar_datos(data)
    await interaction.response.send_message("✅ URL añadida correctamente.", ephemeral=True)

class AddUrl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Se registra el comando manualmente al árbol
async def setup(bot):
    await bot.add_cog(AddUrl(bot))
    bot.tree.add_command(addurl)
