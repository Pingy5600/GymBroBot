import discord
import tempfile
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation


def getDiscordTimeStamp(old_timestamp):
    timestamp = int(old_timestamp.timestamp())
    return f"<t:{timestamp}:D>"

async def setGraph(POOL, loop, message, users_prs, embed):
    file = await loop.run_in_executor(POOL, generate_graph, users_prs)
    embed.set_image(url="attachment://graph.gif")

    await message.edit(embed=embed, attachments=[file])

def generate_graph(users_prs):

    # Prepare the data
    colors = ['#2a9d8f', '#e76f51', "r", "c", "m", "y", "k"]  # Possible colors
    background_color = '#fef9ef'

    # Sort and structure data
    # TODO interpolate points so we have at lease 50 'prs'
    user_data = []
    for idx, (user, prs) in enumerate(users_prs):
        prs.sort(key=lambda x: x[2])  # Sort PRs by date
        dates = [pr[2] for pr in prs]
        weights = [pr[1] for pr in prs]
        color = colors[idx % len(colors)]
        user_data.append((user.display_name, dates, weights, color))

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

        # plot data
        for user, dates, weights, color in user_data:
            subset_dates = dates[:max(1, frame)]
            subset_weights = weights[:max(1, frame)]

            line, = ax.plot(
                subset_dates, subset_weights,
                marker="o", linestyle="-", color=color, label=user
            )

            for i in range(len(dates)):
                plt.annotate(
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
    
    interval = 600
    max_frames = max(len(dates) for _, dates, _, _ in user_data) + 1
    hold_duration = 5000  # Hold duration for the last frame in ms
    hold_frames = int(hold_duration / interval)


    # Add extra frames for holding the last frame
    extended_frames = chain(range(max_frames), [max_frames - 1] * hold_frames)
    
    ani = FuncAnimation(
        fig=fig,
        func=update,
        frames=max_frames,
        interval=300, # in ms
        blit=False,
        repeat=False
    )

    plt.legend(title="Users")
    
    # Save the GIF to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".gif") as temp_file:
        ani.save(temp_file.name, writer="pillow")
        temp_file.seek(0)
        discord_file = discord.File(temp_file.name, filename='graph.gif')

    plt.close()

    return discord_file

