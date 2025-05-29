

from discord import Interaction, app_commands

def check_top_role():
    async def predicate(interaction: Interaction) -> bool:
        if not interaction.guild:
            await interaction.response.send_message("Este comando solo puede usarse en un servidor.", ephemeral=True)
            return False

        top_role = sorted(interaction.guild.roles, key=lambda r: r.position, reverse=True)[0]
        user_roles = interaction.user.roles if hasattr(interaction.user, "roles") else []
        if top_role not in user_roles:
            await interaction.response.send_message(
                f"🚫 No tienes permisos para usar este comando. Solo el rol más alto del servidor puede ejecutarlo: **{top_role.name}**",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)
