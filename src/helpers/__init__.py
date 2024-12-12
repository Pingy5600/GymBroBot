from .graph import *

def getDiscordTimeStamp(old_timestamp):
    timestamp = int(old_timestamp.timestamp())
    return f"<t:{timestamp}:D>"

# https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix
