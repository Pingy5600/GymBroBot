from embeds import DefaultEmbed
from .__init__ import getDiscordTimeStamp

def calculate_1rm_table(one_rep_max):
    """
    Calculates weight and reps based on 1RM percentages.

    Args:
        one_rep_max (float): The user's one-rep max weight.

    Returns:
        list of dict: A list of rows containing percentage, weight, and reps.
    """
    percentages = [
        (100, 1),
        (95, 2),
        (90, 4),
        (85, 6),
        (80, 8),
        (75, 10),
        (70, 12),
        (65, 16),
        (60, 20),
        (55, 24),
        (50, 30),
    ]
    
    table = []
    for percentage, reps in percentages:
        weight = round(one_rep_max * (percentage / 100), 1)  # Round to 1 decimal place
        table.append({
            "percentage": f"{percentage}%",
            "weight": f"{weight} kg",
            "reps": reps,
        })
    return table


def create_1rm_table_embed(one_rep_max, date):
    """
    Creates a Discord embed with a 1RM table.

    Args:
        one_rep_max (float): The user's one-rep max weight.

    Returns:
        discord.Embed: The embed containing the 1RM table.
    """
    table_data = calculate_1rm_table(float(one_rep_max))

    embed = DefaultEmbed(
        title="📊 1RM Percentage Table",
        description=f"Based on a 1RM of **{one_rep_max} kg** achieved on {getDiscordTimeStamp(date)}",
    )
    
    # Format the table
    table = "```"
    table += f"{'Percentage':<15}{'Lift Weight':<15}{'Reps':<10}\n"
    table += "-" * 40 + "\n"
    for row in table_data:
        table += f"{row['percentage']:<15}{row['weight']:<15}{row['reps']:<10}\n"
    table += "```"

    embed.add_field(name="Workout Plan", value=table, inline=False)
    return embed