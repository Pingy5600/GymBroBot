import tempfile
from datetime import datetime
from itertools import groupby

import discord
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, ImageMagickWriter
from matplotlib.patches import Patch

from databank import db_manager

# Specifieke kleurtoewijzing voor bepaalde gebruikers-ID's
COLOR_MAP = {
    "464400950702899211": "#4169e1",
    "462932133170774036": "#ff0000",
    "559715606014984195": "#084808",
    "733845345225670686": "#2ecc71",
    "334371900170043402": "#fe6900",
    "222415043550117888": "#fff200",
    "548544519793016861": "#30D5C8",
}

FALLBACK_COLORS = ['#2a9d8f', '#e76f51', 'r', 'c', 'm', 'y', 'k']
BACKGROUND_COLOR = '#fef9ef'

async def setGraph(POOL, loop, message, users_prs, embed):
    file = await loop.run_in_executor(POOL, generate_graph, users_prs)
    embed.set_image(url="attachment://graph.gif")

    await message.edit(embed=embed, attachments=[file])


async def set3DGraph(POOL, loop, message, users, exercise, embed):

    data = []
    for user in users:
        prs = await db_manager.get_prs_with_reps(str(user.id), exercise)
        if prs and prs[0] != False:  # Controleer op fouten
            for pr in prs:
                # Converteer naar float voor compatibiliteit
                data.append((
                    user,
                    int(pr['reps']),                          # Aantal reps als integer
                    float(pr['lifted_at'].timestamp()),       # Datum als float-timestamp
                    float(pr['weight'])                      # Gewicht als float
                ))

    file = await loop.run_in_executor(POOL, generate_3d_graph, data)
    if type(file) == str:
        print(file)
        return
    embed.set_image(url="attachment://3d_graph.gif")
    embed.set_footer(text=f"")

    await message.edit(embed=embed, attachments=[file])


def generate_graph(users_prs):

    # Structuur van de data
    user_data = []
    fallback_index = 0

    for idx, (user, prs) in enumerate(users_prs):
        prs.sort(key=lambda x: x[2])  # Sorteer PR's op datum
        dates = [pr[2] for pr in prs]
        weights = [pr[1] for pr in prs]

        # Gebruik een specifieke kleur als die beschikbaar is, anders een fallback
        color = COLOR_MAP.get(str(user.id), FALLBACK_COLORS[fallback_index % len(FALLBACK_COLORS)])
        if str(user.id) not in COLOR_MAP:
            fallback_index += 1

        user_data.append((user.display_name, dates, weights, color))

    # Flatten de data zodat elk frame overeenkomt met data
    flattened_data = []
    for user, dates, weights, color in user_data:
        for date, weight in zip(dates, weights):
            flattened_data.append((date, weight, user, color))

    # Sorteer de platte data op datum
    flattened_data.sort(key=lambda x: x[0])

    # Maak de figuur en as
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.set_facecolor(BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    ax.grid(True)

    def update(frame):
        ax.clear()
        ax.set_facecolor(BACKGROUND_COLOR)
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight (kg)")
        ax.grid(True)

        lines = []
        users_in_lines = set()

        # Groepeer data per gebruiker voor het plotten van lijnen
        user_points = {}
        for date, weight, user, color in flattened_data[:frame + 1]:
            if user not in user_points:
                user_points[user] = {'dates': [], 'weights': [], 'color': color}
            user_points[user]['dates'].append(date)
            user_points[user]['weights'].append(weight)

        for user, data in user_points.items():
            dates = data['dates']
            weights = data['weights']
            color = data['color']

            # Plot de lijn die punten verbindt
            line, = ax.plot(dates, weights, marker="o", linestyle="-", color=color, label=user)

            # Annoteer het laatste punt
            for i in range(len(dates)):
                ax.annotate(
                    f"{weights[i]:.2f} kg",
                    (dates[i], weights[i]),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha="center",
                    fontsize=8,
                    color="black",
                    bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3")
                )

            if user not in users_in_lines:
                lines.append(line)
                users_in_lines.add(user)

        ax.legend(handles=lines, loc='upper left')

        return ax

    ani = FuncAnimation(
        fig=fig,
        func=update,
        frames=len(flattened_data),
        interval=500,  # in ms
        blit=False,
        repeat=False
    )

    plt.legend(title="Users")

    # Sla de GIF op naar een tijdelijk bestand
    with tempfile.NamedTemporaryFile(suffix=".gif") as temp_file:
        ani.save(temp_file.name, writer=ImageMagickWriter(fps=5, extra_args=['-loop', '1']))
        temp_file.seek(0)
        discord_file = discord.File(temp_file.name, filename='graph.gif')

    plt.close()

    return discord_file


def generate_3d_graph(data):
    # Haal data van alle gebruikers op
    if not data:
        return "No data found for the specified users and exercise."
    
    # Data voorbereiden voor plotting
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(BACKGROUND_COLOR)

    legend_labels = []
    legend_handles = []
    
    fallback_index = 0  # Index voor fallback kleuren

    for user, user_data in groupby(sorted(data, key=lambda x: x[0].display_name), key=lambda x: x[0]):
        user_data = list(user_data)  # Maak van de iterator een lijst
        if not user_data:
            continue  # Sla lege datasets over

        user_reps = [pr[1] for pr in user_data]
        user_dates = [pr[2] for pr in user_data]
        user_weights = [pr[3] for pr in user_data]
        
        # Gebruik een specifieke kleur als die beschikbaar is, anders een fallback
        # get user id from user_data
        color = COLOR_MAP.get(str(user.id), FALLBACK_COLORS[fallback_index % len(FALLBACK_COLORS)])
        if str(user.id) not in COLOR_MAP:
            fallback_index += 1

        # Gebruik plot_trisurf om de punten te verbinden
        ax.plot_trisurf(user_reps, user_dates, user_weights, color=color, alpha=0.8) # alpha is transparantie

        # Voeg de gebruikersnaam toe aan de legenda
        legend_labels.append(user_data[0][4] if len(user_data[0]) > 4 else user.display_name)
        legend_handles.append(Patch(color=color, label=legend_labels[-1]))

    # Assen labels instellen
    ax.set_xlabel("Reps")
    ax.set_ylabel("Date")
    ax.set_zlabel("Weight (kg)")

    # Bereken begin-, midden- en einddatums
    unique_dates = sorted(set(pr[2] for pr in data))  # Unieke datums ophalen
    if len(unique_dates) >= 2:
        start_date = unique_dates[0]
        end_date = unique_dates[-1]
        mid_date = (start_date + end_date) / 2  # Gemiddelde tijdstempel
        sampled_dates = [start_date, mid_date, end_date]
    else:
        sampled_dates = unique_dates  # Als er minder dan 2 datums zijn

    # Stel ticks en labels in
    ax.set_yticks(sampled_dates)
    ax.set_yticklabels([datetime.fromtimestamp(date).strftime('%Y-%m-%d') for date in sampled_dates])

    ax.legend(legend_handles, legend_labels, loc="upper left", title="Users")

    def update(frame):
        ax.view_init(elev=30, azim=frame)  # Rotate azimuthal angle
        return [ax]

    ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 5), blit=False)
    
    # Save the GIF to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".gif") as temp_file:
        ani.save(temp_file.name)
        temp_file.seek(0)
        discord_file = discord.File(temp_file.name, filename='3d_graph.gif')

    plt.close()

    return discord_file