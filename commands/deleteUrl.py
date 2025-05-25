import json
import discord
from discord.ext import commands
from discord import app_commands
from .json_dbp import guardar_datos, cargar_datos


class DeleteUrl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

 
    async def autocompletar_urls(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = cargar_datos()
        server_id = str(interaction.guild_id)
        user_id = str(interaction.user.id)

        choices = []
        if server_id in data and user_id in data[server_id]:
            urls = data[server_id][user_id].get("urls", [])
            # Filtrar según lo que el usuario está escribiendo (current)
            for url in urls:
                if current.lower() in url.lower():
                    choices.append(app_commands.Choice(name=url, value=url))

        # Discord permite máximo 25 sugerencias
        return choices[:25]

    @app_commands.command(name="removeurl", description="Eliminar una URL guardada para este servidor")
    @app_commands.describe(url="La URL que quieres eliminar")
    @app_commands.autocomplete(url=autocompletar_urls)
    async def remove_url(self, interaction: discord.Interaction, url: str):
        data = cargar_datos()
        server_id = str(interaction.guild_id)
        user_id = str(interaction.user.id)

        if server_id in data and user_id in data[server_id]:
            urls = data[server_id][user_id].get("urls", [])
            new_url = url if url.startswith("http") else f"https://{url}"

            if new_url in urls:
                urls.remove(new_url)
                guardar_datos(data)
                await interaction.response.send_message(f"✅ La URL '{url}' fue eliminada.", ephemeral=True)
            else:
                await interaction.response.send_message("⚠️ La URL no está en tu lista.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No tienes URLs guardadas en este servidor.", ephemeral=True)

# Registrar el Cog
async def setup(bot):
    await bot.add_cog(DeleteUrl(bot))
