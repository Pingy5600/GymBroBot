from typing import List
import discord
from discord.ext import commands

from checks import is_admin_or_has_permissions
import embeds
from databank import db_manager
from helpers.badges import add_badges_field_to_embed, get_user_badges, badge_autocomplete, grant_badge
from shop import Shop


class ShopCog(commands.Cog, name="shop"):
    def __init__(self, bot):
        self.bot = bot
        self.title = "💸 Shop"


    @discord.app_commands.command(name="grant_badge", description="Grant a user a badge")
    @discord.app_commands.describe(user="Which user", badge="Which badge")
    @discord.app_commands.autocomplete(badge=badge_autocomplete)
    @is_admin_or_has_permissions()
    async def grant_badge(self, interaction: discord.Interaction, user: discord.User, badge: str):
        await interaction.response.defer(thinking=True)
        badge_granted = await grant_badge(user, badge)

        embed = embeds.DefaultEmbed(
            title=badge_granted,
            user=user
        )

        await interaction.followup.send(embed=embed)
        

    @discord.app_commands.command(name="shop", description="Opens the shop")
    async def shop(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        shop = Shop()
        
        # Genereer en stuur de embed
        embed = embeds.DefaultEmbed(
            title="💸 Shop"
        )

        embed.add_field(
            name="Available Items",
            value='\n'.join(str(item) for item in shop.get_available_items_for_user(interaction.user))
        )

        await interaction.followup.send(embed=embed)

    @discord.app_commands.command(name="badges", description="See all badges")
    async def badges(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        embed = embeds.DefaultEmbed(
            "🪪 Badges",
        )

        badges = await db_manager.get_all_badges()
        owned_badges = await get_user_badges(interaction.user.id)

        embed = add_badges_field_to_embed(embed, badges, owned_badges)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ShopCog(bot))
