""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import discord
import embeds

from discord import app_commands
from discord.ext import commands
from exceptions import CogLoadError


class Admin(commands.Cog, name="admin"):
    def __init__(self, bot):
        self.bot = bot

    command_cog_group = app_commands.Group(name="cog", description="Cog Group")

    # TODO: add checks

    @app_commands.command(
        name="sync",
        description="Synchronizes the slash commands (admin only)",
    )
    @app_commands.describe(scope="The scope of the sync.")
    @app_commands.choices(scope=[
        discord.app_commands.Choice(name="Global", value="global"),
        discord.app_commands.Choice(name="Server", value="server"),
    ])
    async def sync(self, interaction, scope: discord.app_commands.Choice[str]) -> None:
        """Synchronizes the slash commands

        Args:
            interaction (Interaction): Users interaction
            scope (discord.app_commands.Choice[str]): The scope to sync, can be global or server
        """
        await interaction.response.defer()

        if scope.value == "global":
            cmds = await self.bot.tree.sync()
            self.bot.save_ids(cmds)

            return await interaction.followup.send(embed=embeds.OperationSucceededEmbed(
                "Slash commands have been globally synchronized."
            ))

        elif scope.value == "server":

            # context.bot.tree.copy_global_to(guild=context.guild)
            cmds = await self.bot.tree.sync(guild=interaction.guild)
            self.bot.save_ids(cmds)

            return await interaction.followup.send(embed=embeds.OperationSucceededEmbed(
                "Slash commands have been synchronized in this server."
            ))
            

        await interaction.followup.send(embed=embeds.OperationFailedEmbed(
            "The scope must be 'global' or 'server'"
        ))



    @command_cog_group.command(
        name="load",
        description="Load a cog (admin only)",
    )
    @app_commands.describe(cog="The name of the cog to load")
    async def load_cog(self, interaction, cog: str) -> None:
        """Load a given cog

        Args:
            interaction (Interaction): users interaction
            cog (str): The cog to load
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            self.bot.loaded.add(cog)
            self.bot.unloaded.discard(cog)

        except Exception:
            raise CogLoadError(cog, 0)

        await interaction.response.send_message(embed=embeds.OperationSucceededEmbed(
            f"Successfully loaded the `{cog}` cog."
        ))



    @command_cog_group.command(
        name="unload",
        description="Unloads a cog (admin only)",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    async def unload_cog(self, interaction, cog: str) -> None:
        """Unloads a cog

        Args:
            interaction (Interaction): Users Interaction
            cog (str): The cog to unload
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            self.bot.loaded.discard(cog)
            self.bot.unloaded.add(cog)
        except Exception:
            raise CogLoadError(cog, 1)

        await interaction.response.send_message(embed=embeds.OperationSucceededEmbed(
            f"Successfully unloaded the `{cog}` cog."
        ))



    @command_cog_group.command(
        name="reload",
        description="Reloads a cog (admin only)",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    async def reload_cog(self, interaction, cog: str) -> None:
        """Reloads a cog

        Args:
            interaction (Interaction): Users interaction
            cog (str): The cog to reload
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")

        except Exception:
            raise CogLoadError(cog, 2)

        await interaction.response.send_message(embed=embeds.OperationSucceededEmbed(
            f"Successfully reloaded the `{cog}` cog."
        ))


    @command_cog_group.command(
        name="all",
        description="See loaded/unloaded cogs (admin only)",
    )
    async def all(self, interaction) -> None:
        """Shows which cogs are loaded/unloaded

        Args:
            interaction (Interaction): users interaction
        """
        embed = embeds.DefaultEmbed(
            "Cog Info"
        )
        loaded_fields = "\n".join(list(self.bot.loaded))
        embed.add_field(
            name="Loaded", value=f'```\n{loaded_fields}```', inline=False
        )

        unloaded_fields = "\n".join(list(self.bot.unloaded))
        if len(unloaded_fields) > 0:
            embed.add_field(
                name="Unloaded", value=f"```\n{unloaded_fields}```", inline=False
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
