import asyncio
import math
from concurrent.futures import ThreadPoolExecutor

import dateparser
import discord
from discord.ext import commands

from databank import db_manager
from embeds import DefaultEmbed, OperationFailedEmbed
from helpers import (EXERCISE_CHOICES, create_1rm_table_embed,
                     getDiscordTimeStamp, getImageFromExercise, set3DGraph)

POOL = ThreadPoolExecutor()

class Rep(commands.Cog, name="rep"):
    def __init__(self,bot):
        self.bot = bot

    command_rep_group = discord.app_commands.Group(name="rep", description="rep Group")

    @command_rep_group.command(name="calculator", description="Calculate the amount of reps you should do for your 1RM")
    @discord.app_commands.describe(exercise="which exercise", user="Which user")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def rep_calc(self, interaction: discord.Interaction, exercise: str, user: discord.User=None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        # get 1RM for that exercise for user
        try:
            success, resultsOrErr = await db_manager.getMaxOfUserWithExercise(str(user.id), exercise)
            if not success: raise ValueError(resultsOrErr)

            embed = create_1rm_table_embed(*resultsOrErr)
            embed.set_thumbnail(url=getImageFromExercise(exercise))

        except Exception as err:
            embed = OperationFailedEmbed(
                description=f"An error has occurred: {err}"
            )

        return await interaction.followup.send(embed=embed)
    
    @command_rep_group.command(name="add", description="Adds reps for a specific exercise and weight")
    @discord.app_commands.describe(
        date="The date of the reps",
        reps="The number of reps",
        weight="The weight lifted",
        exercise="Which exercise",
        user="Which user"
    )
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def add_reps(
        self,
        interaction: discord.Interaction,
        reps: int,
        weight: str,
        exercise: str,
        date: str = None,
        user: discord.User = None
    ):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        if date is None:
            date = "vandaag"

        reps_cleaned = weight.replace(',', '.')
        reps_command_ref = f"</add_reps:{self.bot.tree.get_command('rep').id}>"

        try:
            pr = float(reps_cleaned)

        except ValueError:
            embed = OperationFailedEmbed(
                description=
                "You provided an invalid PR value. Please use the correct format.\n"
                f"Please try again: {reps_command_ref}"
            )
            return await interaction.followup.send(embed=embed)

        try:
            # Controleer of reps een integer is
            reps = int(reps)
            if reps <= 0:
                raise ValueError("The number of reps must be greater than 0.")

            # Controleer of weight een float is
            weight = float(weight)
            if weight <= 0:
                raise ValueError("The weight must be greater than 0.")

        except ValueError as e:
            embed = OperationFailedEmbed(
                description=f"Invalid input: {e}\nPlease try again: {reps_command_ref}"
            )
            return await interaction.followup.send(embed=embed)

        try:
            # Datum verwerken
            date_obj = dateparser.parse(date, settings={
                'DATE_ORDER': 'DMY',
                'TIMEZONE': 'CET',
                'PREFER_DAY_OF_MONTH': 'first',
                'PREFER_DATES_FROM': 'past',
                'DEFAULT_LANGUAGES': ["en", "nl"]
            })

            if date_obj is None:
                raise ValueError("Invalid date format")

        except ValueError:
            embed = OperationFailedEmbed(
                description=(
                    "Invalid date. Use a format like '2024-11-25' or 'November 25, 2024'.\n"
                    f"Please try again: {reps_command_ref}"
                )
            )
            return await interaction.followup.send(embed=embed)

        except Exception as e:
            embed = OperationFailedEmbed(description=f"An error has occurred: {e}")
            return await interaction.followup.send(embed=embed)

        # Voeg de reps toe aan de database
        resultaat = await db_manager.add_reps(user.id, exercise, weight, reps, date_obj)

        if resultaat[0]:
            embed = DefaultEmbed(
                title="Reps Added!",
                description=f"Added {reps} reps at {weight}kg for {exercise.capitalize()}."
            )
            embed.add_field(name="User", value=user.mention, inline=True)
            embed.add_field(name="Exercise", value=exercise, inline=True)
            embed.add_field(name="Date", value=getDiscordTimeStamp(date_obj), inline=True)
            embed.set_thumbnail(url=getImageFromExercise(exercise))
            return await interaction.followup.send(embed=embed)

        embed = OperationFailedEmbed(description=f"Something went wrong: {resultaat[1]}")
        await interaction.followup.send(embed=embed)


    @command_rep_group.command(name="list", description="Gives reps of the given user")
    @discord.app_commands.describe(user="Which user", exercise="Which exercise")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def list(self, interaction: discord.Interaction, exercise: str, user: discord.User = None):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        try:
            reps = await db_manager.get_prs_with_reps(str(user.id), exercise)

            if len(reps) == 0:
                embed = OperationFailedEmbed(
                    description=f"No reps found for the specified exercise."
                )
                return await interaction.followup.send(embed=embed)

            elif reps[0] == -1:
                raise Exception(reps[1])

        except Exception as e:
            embed = OperationFailedEmbed(
                description=f"An error has occurred: {e}"
            )
            return await interaction.followup.send(embed=embed)

        view = RepPaginator(reps, exercise, user)
        embed = view.generate_embed()
        embed.set_thumbnail(url=getImageFromExercise(exercise))
        await interaction.followup.send(embed=embed, view=view)


    @command_rep_group.command(name="delete", description="Delete specific reps")
    @discord.app_commands.describe(exercise="Exercise", user="User whose reps to delete")
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def delete(
        self, 
        interaction: discord.Interaction, 
        exercise: str, 
        user: discord.User = None
    ):
        await interaction.response.defer(thinking=True)

        if user is None:
            user = interaction.user

        if user != interaction.user and not interaction.user.guild_permissions.administrator:
            embed = OperationFailedEmbed(
                description="You do not have permission to delete reps for other users."
            )
            return await interaction.followup.send(embed=embed)

        try:
            reps_data = await db_manager.get_prs_with_reps(str(user.id), exercise)

            if len(reps_data) == 0:
                embed = OperationFailedEmbed(description="No reps found for the specified exercise.")
                return await interaction.followup.send(embed=embed)
            elif reps_data[0] == -1:
                raise Exception(reps_data[1])

            paginator = RepPaginator(reps_data, exercise, user)
            embed = paginator.generate_embed()
            content = "Reply with the **number** of the rep you want to delete."
            message = await interaction.followup.send(content=content, embed=embed, view=paginator)

            # Save the message_id
            message_id = message.id

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel and m.content.isdigit() and m.reference is not None and m.reference.message_id == message_id

            msg = await self.bot.wait_for("message", check=check, timeout=60.0)
            index = int(msg.content) - 1

            if index < 0 or index >= len(reps_data):
                raise ValueError("Invalid selection. Please try again.")

            selected_rep = reps_data[index]
            result, err = await db_manager.delete_reps(str(user.id), exercise, selected_rep['weight'], selected_rep['lifted_at'])
            if not result:
                raise Exception(err)

            embed = DefaultEmbed(
                title="Reps Deleted",
                description=f"Successfully deleted **{selected_rep['reps']} reps** of **{int(selected_rep['weight'])} kg** on {getDiscordTimeStamp(selected_rep['lifted_at'])}."
            )
            await interaction.followup.send(embed=embed)

        except asyncio.TimeoutError:
            embed = OperationFailedEmbed(description="You took too long to respond! Command cancelled.")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = OperationFailedEmbed(description=f"An error occurred: {e}")
            await interaction.followup.send(embed=embed)


    @command_rep_group.command(name="graph", description="Genereer een 3D-plot van PRs.")
    @discord.app_commands.describe(
        exercise="Which exercise",
        user1="First user",
        user2="Second user (optional)",
        user3="Third user (optional)"
    )
    @discord.app_commands.choices(exercise=EXERCISE_CHOICES)
    async def three_d_plot(
        self,
        interaction: discord.Interaction,
        exercise: str,
        user1: discord.User = None,
        user2: discord.User = None,
        user3: discord.User = None
    ):
        await interaction.response.defer(thinking=True)

        # Gebruikers toevoegen aan de lijst
        users = [user for user in [user1, user2, user3] if user]
        if not users:
            users.append(interaction.user)

        embed = DefaultEmbed(
            title=f"{exercise.capitalize()} PR Graph",
            description=f"Here's the 3D graph for {', '.join(user.display_name for user in users)}."
        )
        embed.set_footer(text="This may take a while...")
        message = await interaction.followup.send(embed=embed)

        loop = asyncio.get_event_loop()
        loop.create_task(
            set3DGraph(POOL, loop, message, users, exercise, embed)
        )



class RepPaginator(discord.ui.View):
    def __init__(self, reps, exercise, user):
        super().__init__()
        self.reps = reps
        self.exercise = exercise
        self.user = user
        self.current_page = 0
        self.items_per_page = 10
        self.max_pages = math.ceil(len(reps) / self.items_per_page)

        if self.max_pages <= 1:
            self.clear_items()  # If only 1 page, remove buttons entirely

    def generate_embed(self):
        embed = DefaultEmbed(
            title=f"{self.exercise.capitalize()} Reps of {self.user.display_name}",
        )

        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_reps = self.reps[start:end]

        for idx, rep in enumerate(page_reps, start=start + 1):  # Voeg nummers toe aan de reps
            weight = rep['weight']
            reps = rep['reps']
            timestamp = getDiscordTimeStamp(rep['lifted_at'])

            # Format weight to two decimal places if it is a decimal number
            if weight % 1 != 0:  # If it is a decimal
                weight = f"{weight:.2f}"
            else:
                weight = f"{int(weight)}"  # Remove decimals if it's an integer

            embed.add_field(
                name=f"{idx}. {timestamp}",  # Nummer voor de datum
                value=f"**Weight:** {weight} kg | **Reps:** {reps}",
                inline=False
            )

        embed.set_footer(text=f"Page {self.current_page + 1} of {self.max_pages}")
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            embed = self.generate_embed()
            self.update_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            embed = self.generate_embed()
            self.update_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        # Disable buttons based on the current page
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.max_pages - 1

        # If there's only one page, remove the buttons completely
        if self.max_pages <= 1:
            self.clear_items()  # Remove the buttons if there's only 1 page

async def setup(bot):
    await bot.add_cog(Rep(bot))