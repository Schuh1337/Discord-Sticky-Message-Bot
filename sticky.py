import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Ready: {bot.user.name} | {bot.user.id}')

ID = () # your user id here, only you will be able to use the commands
max_message_count = 1
message_count = 0
last_sticky_message = None
sticky_message_channel = ""
sticky_message_content = ""

@bot.event
async def on_message(message):
    global last_sticky_message, message_count, sticky_message_channel, sticky_message_content

    if message.author.bot:
        return
    
    if (not message.content.startswith('!') or message.author.id != ID) and sticky_message_content != "":
        if message.channel.id == sticky_message_channel:
            message_count += 1
            if message_count == max_message_count:
                await last_sticky_message.delete()
                last_sticky_message = await message.channel.send(sticky_message_content)
                message_count = 0
        return

    args = message.content[1:].strip().split(' ')
    command = args.pop(0).lower()

    if command == "stick":
        if message.author.id == ID:
            try:
                sticky_message_channel = message.channel.id
                sticky_message_content = ' '.join(args)
                last_sticky_message = await message.channel.send(sticky_message_content)
                await message.delete()
            except Exception as e:
                print(e)

    elif command == "unstick":
        if message.author.id == ID:
            last_sticky_message = None
            message_count = 0
            sticky_message_channel = ""
            sticky_message_content = ""
            await message.delete()

bot.run("bot token here")
