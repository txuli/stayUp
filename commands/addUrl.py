import json
import os
import discord
from discord.ext import commands
from discord import app_commands
from commands.task import status_task

DATA_FILE = 'url.json'

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class AddUrl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addurl", description="Añade una URL al servidor")
    async def addurl(self, interaction: discord.Interaction, url: str):
        print(f"📥 /addurl ejecutado por {interaction.user} con URL: {url}")
        servidor_id = str(interaction.guild_id)
        usuario_id = str(interaction.user.id)
        data = cargar_datos()

        if servidor_id not in data:
            data[servidor_id] = {}

        if usuario_id not in data[servidor_id]:
            data[servidor_id][usuario_id] = {"urls": []}

        new_url = url if url.startswith("http") else f"https://{url}"
        
        if new_url in data[servidor_id][usuario_id]["urls"]:
            embed = discord.Embed(
                title='Url already in use',
                description=f'The URL `{new_url}` is already in the data.',
                color=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        data[servidor_id][usuario_id]["urls"].append(new_url)
        guardar_datos(data)

        embed = discord.Embed(
            title='Add New URL',
            description=f'The URL `{new_url}` was successfully added.',
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

        
        await status_task(self.bot)

# Se registra el comando en el árbol
async def setup(bot):
    await bot.add_cog(AddUrl(bot))
