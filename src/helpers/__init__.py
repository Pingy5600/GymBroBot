def getDiscordTimeStamp(old_timestamp):
    timestamp = int(old_timestamp.timestamp())
    return f"<t:{timestamp}:D>"