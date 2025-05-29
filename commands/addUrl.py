import json
import os
import discord
from discord.ext import commands
from discord import app_commands
from commands.task import status_task

from db import get_connection, db_cursor
from mysql.connector import Error, errorcode

from checks import check_top_role

def cargar_datos(servidor_id):
    with db_cursor(dictionary=True) as cursor:
        sql = "SELECT * FROM servers WHERE id = %s"
        cursor.execute(sql, (servidor_id,))
        return cursor.fetchall()

def newServer(servidor_id):
   
    try:
        with db_cursor() as cursor:
            sql = "INSERT INTO servers(id,userid) VALUES (%s,%s)"
            val=(servidor_id, usuario_id)
            cursor.execute(sql, val)
    except Error as e:
        print("❌ Error al insertar en la base de datos:", e)


def insertUrl(servidor_id, new_url):
    try:
        with db_cursor() as cursor:
            sql = "INSERT INTO url(serverId, url) VALUES(%s, %s)"
            val = (servidor_id, new_url ) 
            cursor.execute(sql, val)
            embed = discord.Embed(
                title='Add New URL',
                description=f'The URL `{new_url}` was successfully added.',
                color=discord.Color.blue()
            )
            return embed
    except Error as er:
        print("❌ Error inserting into database:", er)
        if er.errno == errorcode.ER_DUP_ENTRY:
            embed = discord.Embed(
                title='Url already in use',
                description=f'The URL `{new_url}` is already in the data.',
                color=discord.Color.yellow()
            )
            return embed
            
        


class AddUrl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addurl", description="Add a URL to the server")
    @check_top_role()
    async def addurl(self, interaction: discord.Interaction, url: str):
        print(f"📥 /addurl executed by {interaction.user} with URL: {url}")
        servidor_id = interaction.guild_id
        usuario_id = str(interaction.user.id)
        data = cargar_datos(servidor_id)
        print(data)
        if not data:
            newServer(servidor_id)
        
        new_url = url if url.startswith("http") else f"https://{url}"
        embed=insertUrl(servidor_id, new_url)
           
        
       
        await interaction.response.send_message(embed=embed, ephemeral=True)

        
        await status_task(self.bot)


async def setup(bot):
    await bot.add_cog(AddUrl(bot))
