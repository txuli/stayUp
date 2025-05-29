import discord
from discord.ext import commands
from discord import app_commands
from commands.task import status_task
from db_queries import obtener_urls_autocompletado, eliminar_url  # Asegúrate de tener estas funciones
from db import db_cursor 
from checks import check_top_role
class DeleteUrl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Register the command with autocompletion
        remove_cmd = app_commands.Command(
            name="removeurl",
            description="Eliminar una URL guardada para este servidor",
            callback=self.remove_url,
        )
        remove_cmd.autocomplete("url")(self.autocompletar_urls)
        self.bot.tree.add_command(remove_cmd)

    # URL AUTOCOMPLETION
    
    async def autocompletar_urls(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        servidor_id = interaction.guild_id

        with db_cursor(dictionary=True) as cursor:
            sql = "SELECT url FROM url WHERE serverId = %s LIMIT 25"
            cursor.execute(sql, (servidor_id,))
            urls = [row["url"] for row in cursor.fetchall()]

            return [app_commands.Choice(name=url, value=url) for url in urls]


    
    @check_top_role()
    async def remove_url(self, interaction: discord.Interaction, url: str):
        servidor_id = interaction.guild_id
        usuario_id = interaction.user.id
        new_url = url if url.startswith("http") else f"https://{url}"

        eliminada = eliminar_url(servidor_id, new_url)

        if eliminada:
            embed = discord.Embed(
                title='✅ URL deleted',
                description=f'The URL `{new_url}` was deleted succesfully.',
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title='❌ No encontrada',
                description=f'The URL `{new_url}` is not registered in your account.',
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)
        await status_task(self.bot)


async def setup(bot):
    await bot.add_cog(DeleteUrl(bot))
