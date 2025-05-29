import discord
from discord.ext import commands
from discord import app_commands
import requests
from datetime import datetime
from db_queries import cargar_urls
from zoneinfo import ZoneInfo
from checks import check_top_role

class StatusServ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @app_commands.command(name="statusserv", description="Verifica el estado de una URL o todas las guardadas")
    @app_commands.describe(url="(opcional) URL individual a verificar")
    @check_top_role()
    async def status_serv(self, interaction: discord.Interaction, url: str = None):
        print(f"🔍 Running /statusserv command for the server{interaction.guild_id}")
        servidor_id = str(interaction.guild_id)
        if not url:
            data = cargar_urls(servidor_id)
        else:
            new_url = url if url.startswith("http") else f"https://{url}"
            data = [{"url": new_url, "userId": interaction.user.id}]

            
        print(data)
        if not data:
            await interaction.response.send_message("no data for this server", ephemeral=True)
            return

        else:
            resultado_urls =[]
            for item in data:
                print("entra al for")
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
                title="🔎 Status of URLs",
                description="\n".join(resultado_urls) if resultado_urls else "No URLs were found to review.",
                color=discord.Color.red() if any("error2" in r for r in resultado_urls) else discord.Color.blue(),
            )
            embed.set_footer(text=f"Last fetch: {hora_espana.strftime('%Y-%m-%d %H:%M:%S')}")
            
        
        
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        
        

async def setup(bot):
   
    await bot.add_cog(StatusServ(bot))
   