import discord
from discord.ext import commands

import embeds
from databank import db_manager
from shop import Shop


class ShopCog(commands.Cog, name="shop"):
    def __init__(self, bot):
        self.bot = bot
        self.title = "💸 Shop"


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

        categories = {
            "Common": [],
            "Rare": [],
            "Epic": [],
            "Legendary": [],
        }

        rarity_emojis = {
            "Common": "⭐",
            "Rare": "💪",
            "Epic": "⚡",
            "Legendary": "💎",
        }

        for _, name, desc, icon_url, rarity in badges:
            category = categories.get(rarity, [])
            category.append(f"{icon_url} **{name}** - {desc}")

        for rarity, badge_list in categories.items():
            if badge_list:
                emoji = rarity_emojis.get(rarity)
                embed.add_field(name=f"{emoji} {rarity}", value="\n".join(badge_list), inline=False)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ShopCog(bot))