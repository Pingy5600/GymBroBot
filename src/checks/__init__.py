import os
import discord
from discord.app_commands import check
from discord import Interaction
from exceptions import NoPermission, WrongChannel
from typing import Callable, TypeVar


T = TypeVar("T")
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

def not_in_dm() -> Callable[[T], T]:

    async def predicate(interaction):

        if isinstance(interaction.channel, discord.channel.DMChannel):
            raise WrongChannel("You cannot use this command in dm, use /invite to get an invite")
        return True
    
    return discord.app_commands.check(predicate)

def in_correct_server() -> Callable[[T], T]:

    async def predicate(interaction):

        if interaction.guild_id not in [int(os.environ.get("GUILD_ID")),] and not isinstance(interaction.channel, discord.channel.DMChannel):
            raise WrongChannel("You are only able to use this command in the main server, use /invite to get an invite")
        return True
    
    return discord.app_commands.check(predicate)