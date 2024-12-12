import discord
import tempfile
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, ImageMagickWriter

async def setGraph(POOL, loop, message, users_prs, embed):
    file = await loop.run_in_executor(POOL, generate_graph, users_prs)
    embed.set_image(url="attachment://graph.gif")

    await message.edit(embed=embed, attachments=[file])


def generate_graph(users_prs):

    # Prepare the data
    colors = ['#2a9d8f', '#e76f51', "r", "c", "m", "y", "k"]  # Possible colors
    background_color = '#fef9ef'

    # structure data
    user_data = []
    for idx, (user, prs) in enumerate(users_prs):
        prs.sort(key=lambda x: x[2])  # Sort PRs by date
        dates = [pr[2] for pr in prs]
        weights = [pr[1] for pr in prs]
        color = colors[idx % len(colors)]
        user_data.append((user.display_name, dates, weights, color))

    # flatten it, so each frame has corresponding data
    flattened_data = []
    for user, dates, weights, color in user_data:
        for date, weight in zip(dates, weights):
            flattened_data.append((date, weight, user, color))

    # Sort flattened_data by date
    flattened_data.sort(key=lambda x: x[0])

    # create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    ax.grid(True)

    def update(frame):
        ax.clear()
        ax.set_facecolor(background_color)
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight (kg)")
        ax.grid(True)
        
        lines = []
        users_in_lines = set()

        # Group data by user for plotting lines
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

            # Plot the line connecting points
            line, = ax.plot(dates, weights, marker="o", linestyle="-", color=color, label=user)

            # Annotate the last point
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
        interval=500, # in ms
        blit=False,
        repeat=False
    )

    plt.legend(title="Users")
    
    # Save the GIF to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".gif") as temp_file:
        ani.save(temp_file.name, writer=ImageMagickWriter(fps=5, extra_args=['-loop', '1']))
        temp_file.seek(0)
        discord_file = discord.File(temp_file.name, filename='graph.gif')

    plt.close()

    return discord_file
