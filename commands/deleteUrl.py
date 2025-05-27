import json
import discord
from discord.ext import commands
from discord import app_commands
from .json_dbp import guardar_datos, cargar_datos
from commands.task import status_task

class DeleteUrl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        remove_cmd = app_commands.Command(
            name="removeurl",
            description="Eliminar una URL guardada para este servidor",
            callback=self.remove_url,
        )
        remove_cmd.autocomplete("url")(self.autocompletar_urls)
        self.bot.tree.add_command(remove_cmd)

    async def autocompletar_urls(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = cargar_datos()
        server_id = str(interaction.guild_id)
        user_id = str(interaction.user.id)

        choices = []
        if server_id in data and user_id in data[server_id]:
            urls = data[server_id][user_id].get("urls", [])
            for url in urls:
                if current.lower() in url.lower():
                    choices.append(app_commands.Choice(name=url, value=url))

        return choices[:25]

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
                embed=discord.Embed(
                title='url deletion',
                description=f'the url, {url} was deleted successfully',
                color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed=discord.Embed(
                title='url deletion',
                description=f"the url, {url} was isn't in your data",
                color=discord.Color.red()
                )
                await interaction.response.send_message( mbed=embed, ephemeral=True)
        else:
            embed=discord.Embed(
            title='url deletion',
            description=f"your server hasn't url to remove",
            color=discord.Color.red()
            
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        await status_task(self.bot)   
    
# Registrar el Cog
async def setup(bot):
    await bot.add_cog(DeleteUrl(bot))
