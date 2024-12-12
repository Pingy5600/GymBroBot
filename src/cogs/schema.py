import discord

from discord.ext import commands
from databank import db_manager
from embeds import DefaultEmbed, OperationFailedEmbed

class Schema(commands.Cog, name="schema"):
    def __init__(self,bot):
        self.bot = bot


    @discord.app_commands.command(name="schema", description = "Get the gym schema")
    async def schema(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        try:
            worked, errOrSchema = await db_manager.get_schema()
            if not worked:
                raise ValueError(errOrSchema)
            
            embed = DefaultEmbed(
                '🗓️ Schema'
            )

            for day, desc in errOrSchema.items():
                embed.add_field(name=day,  value=f'```{desc}```', inline=True)

        except Exception as err:
            embed = OperationFailedEmbed(
                "Something went wrong..."
            )

        await interaction.followup.send(embed=embed)


    @discord.app_commands.command(name="schema-edit", description="Edit the schema")
    @discord.app_commands.default_permissions(administrator=True)
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
        
        edit_schema_command_ref = f"</edit_schema:{self.bot.tree.get_command('edit_schema').id}>"
        schema_command_ref = f"</schema:{self.bot.tree.get_command('schema').id}>"

        try:
            worked, err = await db_manager.update_schema(monday, tuesday, wednesday, thursday, friday, saturday, sunday)
            if not worked:
                raise ValueError(err)
            
            embed=DefaultEmbed('Schema updated!', f'Use {schema_command_ref} to see the schema.')
            
        except Exception as err:
            embed = OperationFailedEmbed(
                description=
                "Something went wrong\n"
                f"{err}\n"
                f"Please try again: {edit_schema_command_ref}"
            )

        return await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Schema(bot))