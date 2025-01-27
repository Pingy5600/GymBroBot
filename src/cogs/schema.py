import discord
from discord.ext import commands

from checks import is_admin_or_has_permissions
from databank import db_manager
from embeds import DefaultEmbed


class Schema(commands.Cog, name="schema"):
    def __init__(self,bot):
        self.bot = bot
        self.title = "🕗 Schema"


    @discord.app_commands.command(name="schema", description = "Get the gym schema")
    async def schema(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        worked, errOrSchema = await db_manager.get_schema()
        if not worked:
            raise ValueError(errOrSchema)
        
        embed = DefaultEmbed('🗓️ Schema')

        for day, desc in errOrSchema.items():
            embed.add_field(name=day,  value=f'```{desc}```', inline=True)

        await interaction.followup.send(embed=embed)


    @is_admin_or_has_permissions()
    @discord.app_commands.command(name="schema-edit", description="Edit the schema")
    async def edit_schema(
        self, interaction: discord.Interaction,
        monday: str = None,
        tuesday: str = None,
        wednesday: str = None,
        thursday: str = None,
        friday: str = None,
        saturday: str = None,
        sunday: str = None,
    ):
        await interaction.response.defer(thinking=True)

        if not any([monday, tuesday, wednesday, thursday, friday, saturday, sunday]):
            raise ValueError("Please provide at least one day to edit.")
        
        worked, err = await db_manager.update_schema(monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        if not worked:
            raise ValueError(err)
        
        embed=DefaultEmbed('Schema updated!')

        return await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Schema(bot))