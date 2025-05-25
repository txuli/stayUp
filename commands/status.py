import discord
from discord.ext import commands
from discord import app_commands
import requests
from .json_dbp import cargar_datos

class StatusServ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @app_commands.command(name="statusserv", description="Verifica el estado de una URL o todas las guardadas")
    @app_commands.describe(url="(opcional) URL individual a verificar")
    async def status_serv(self, interaction: discord.Interaction, url: str = None):
        print(f"🔍 Ejecutando comando /statusserv para el servidor {interaction.guild_id}")
        servidor_id = str(interaction.guild_id)
        data = cargar_datos()

        if servidor_id not in data:
            await interaction.response.send_message("no data for this server", ephemeral=True)
            return

        if not url:
            correctas = []
            erroneas = []
            for usuario_id, info in data[servidor_id].items():
                urls = info.get("urls", [])
                for u in urls:
                    try:
                        response = requests.get(u, timeout=5)
                        if response.status_code == 200:
                            correctas.append(u)
                        else:
                            erroneas.append(f"{u} (HTTP {response.status_code})")
                    except:
                        erroneas.append(f"{u} (No se pudo conectar)")

            mensaje = "**✅ URLs accesibles:**\n" + "\n".join(correctas) if correctas else "Ninguna URL accesible."
            mensaje += "\n\n**❌ URLs con error:**\n" + "\n".join(erroneas) if erroneas else "Ninguna URL con error."
            await interaction.response.send_message(mensaje[:2000], ephemeral=True)
        else:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    await interaction.response.send_message(f"✅ {url} está online.")
                else:
                    await interaction.response.send_message(f"⚠️ {url} no responde correctamente (HTTP {response.status_code})")
            except:
                await interaction.response.send_message(f"❌ No se pudo conectar con {url}.")

async def setup(bot):
    print("📦 Intentando cargar el Cog StatusServ...")
    await bot.add_cog(StatusServ(bot))
    print("📦 Cog StatusServ cargado exitosamente.")