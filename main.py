import discord
from discord.ext import commands
import logging
import requests
from dotenv import load_dotenv
import os
import asyncio
from commands.task import status_task
from discord.ext import tasks 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


intents = discord.Intents.default()
intents.message_content = True
intents.presences = True


bot = commands.Bot(command_prefix='!', intents=intents)

@tasks.loop(minutes=1)
async def ejecutar_tarea_status():
    await  status_task(bot)
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    await bot.change_presence(activity=discord.Game(name="!help"))
    ejecutar_tarea_status.start()
    try:
        print("🔄 Cargando Cogs...")
        await bot.load_extension("commands.addUrl")
        await bot.load_extension("commands.status")
        await bot.load_extension("commands.deleteUrl")
        print("✅ Cogs cargados correctamente.")
    except Exception as e:
        print(f"❌ Error al cargar los Cogs: {e}")
        logging.error(f"Error al cargar los Cogs: {e}")


    await asyncio.sleep(5)

    try:
        print("🔄 Iniciando sincronización global de comandos...")
        synced = await bot.tree.sync()
        print(f"✅ Comandos sincronizados globalmente: {[cmd.name for cmd in synced]}")
    except asyncio.TimeoutError:
        print("❌ Error: La sincronización global tomó demasiado tiempo.")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

    
@bot.command()
async def hello(ctx):
    await ctx.send(f'👋 Hello {ctx.author.mention}!')
    try:
        response = requests.get('https://durangaldekobizikletaeskola.com/es', timeout=5)
        if response.status_code == 200:
            await ctx.send('✅ Ping exitoso al sitio web!')
        else:
            await ctx.send(f'⚠️ Código de respuesta: {response.status_code}')
    except requests.RequestException:
        await ctx.send('❌ Error al conectar con el sitio web.')



bot.run(token, log_handler=handler, log_level=logging.INFO)
