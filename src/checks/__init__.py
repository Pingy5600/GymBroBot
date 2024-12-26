from discord.app_commands import check
from discord import Interaction
from exceptions import NoPermission

def is_admin_or_has_permissions():
    def predicate(interaction: Interaction) -> bool:
        has_admin_permission = interaction.user.guild_permissions.administrator
        is_in_list = interaction.user.id in [464400950702899211, 462932133170774036]
        
        if not (has_admin_permission or is_in_list):
            raise NoPermission()
        
        return True
    return check(predicate)
