import discord
from discord.app_commands import check
from discord import Interaction
from exceptions import NoPermission


admin_list = [464400950702899211, 462932133170774036]

def is_admin_or_has_permissions():
    def predicate(interaction: Interaction) -> bool:
        has_admin_permission = interaction.user.guild_permissions.administrator
        is_in_list = interaction.user.id in admin_list
        
        if not (has_admin_permission or is_in_list):
            raise NoPermission()
        
        return True
    return check(predicate)


def is_admin():
    def predicate(interaction: discord.Interaction) -> bool:
        is_in_list = interaction.user.id in admin_list

        if not(is_in_list):
            raise NoPermission()
        
        return True
    return check(predicate)