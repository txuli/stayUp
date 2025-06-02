import requests
import discord
from datetime import datetime
from zoneinfo import ZoneInfo
from db_queries import cargar_urls, cargar_mensaje_db, guardar_mensaje_db  # Update these names in your DB module

async def status_task(bot):
    for guild in bot.guilds:
        server_id = guild.id
        urls = cargar_urls(server_id)

        if not urls:
            continue

        message_info = cargar_mensaje_db(server_id)
        channel = None
        message = None

        # Try to get the previously saved channel
        if message_info and message_info["channel_id"]:
            channel = bot.get_channel(int(message_info["channel_id"]))

        # If there's no registered channel, search for or create "logs" channel
        if not channel:
            # Look for an existing "logs" channel
            existing_channel = discord.utils.get(guild.text_channels, name="logs")
            if existing_channel:
                channel = existing_channel
                print(f"📁 'logs' channel already exists in server {guild.name} ({server_id})")
            else:
                # Create "logs" channel if not found
                try:
                    
                    top_role = max(
                        (role for role in guild.roles if role != guild.default_role),
                        key=lambda r: r.position
                    )

                   
                    stayup_role = discord.utils.get(guild.roles, name="stayUp")

                    
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(view_channel=False),  # Ocultar para todos
                        top_role: discord.PermissionOverwrite(view_channel=True, read_message_history=True),
                    }

                    
                    if stayup_role:
                        overwrites[stayup_role] = discord.PermissionOverwrite(view_channel=True, read_message_history=True)

                   
                    channel = await guild.create_text_channel(
                        name="logs",
                        overwrites=overwrites,
                        reason="Channel created to log URL status updates"
                    )

                    print(f"✅ Created private 'logs' channel in server {guild.name} ({server_id})")

                except discord.Forbidden:
                    print(f"❌ Missing permissions to create channel in {guild.name} ({server_id})")
                    continue

                except Exception as e:
                    print(f"❌ Error creating channel in {guild.name} ({server_id}): {e}")
                    continue

            # Save the channel ID with a placeholder message ID (will be updated below)
            guardar_mensaje_db(server_id, channel.id, message_id)

        # Check each URL
        url_results = []
        for item in urls:
            user_id = item.get("userId")
            mention = f"<@{user_id}>" if user_id else ""
            url = item["url"]
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    url_results.append(f"<a:online:1376996976843030539> {url}")
                else:
                    url_results.append(f"<a:error2:1377008688052830399> {mention} {url} (Status: {response.status_code})")
            except:
                url_results.append(f"<a:error2:1377008688052830399> {mention} {url} (No response)")

        current_time = datetime.now(ZoneInfo("Europe/Madrid"))
        embed = discord.Embed(
            title="🔎 URL Auto-Check",
            description="\n".join(url_results) if url_results else "No URLs found to check.",
            color=discord.Color.red() if any("error2" in r for r in url_results) else discord.Color.blue(),
        )
        embed.set_footer(text=f"Last checked: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Try to edit the previous message
        if message_info and message_info["message_id"]:
            try:
                message = await channel.fetch_message(int(message_info["message_id"]))
                await message.edit(embed=embed)
                continue
            except:
                print(f"⚠️ Could not edit the previous message in channel {channel.id}. A new one will be sent.")

        # Send new message if editing failed
        message = await channel.send(embed=embed)
        guardar_mensaje_db(server_id, channel.id, message.id)
