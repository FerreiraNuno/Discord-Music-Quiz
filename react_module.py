import time


def react(message):
    if message.content.startswith("!rank"):
        time.sleep(0.5)
        return message.channel.send('trash')

    if message.content.startswith("holy shit nigga"):
        return message.channel.send('congrats nigga')

    if str(message.author) in ["Destructiondon#7702", "MinecraftExperteDe#7702"]:
        return message.channel.send('shut up nigga')

    if "nigga" in message.content.lower():
        return message.channel.send('lets gooo!')

    if str(message.author) == "Trash police by Anton#1922":
        return message.channel.send('bruh your bot is trash')

    else:
        pass
