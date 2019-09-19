import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

TOKEN = 'NjIzMjM3OTk4NTI3NjQzNzEx.XX_igQ.cwYvNT1n6Ulr2JYjcV6UqNmHPAg'
pause = False

client = discord.Client()
bot = commands.Bot(command_prefix='#')

@client.event
async def on_message(message):
    print(message.content)
    print(type(message.content))

    global pause


    if "unkill" in message.content:
        pause = False
        msg = 'Ah not dead anymore'.format(message)
        await client.send_message(message.channel, msg)
            

    
    if not pause:

        # we do not want the bot to reply to itself
        if message.author == client.user:
            return

        if "steven" in message.content:
            msg = 'Hello {0.author.mention}, Im StevenIm'.format(message)
            await client.send_message(message.channel, msg)

        if "but" in message.content:     
            if "ping" in message.content:
                msg = 'but but but but... {0.author.mention} IS RACIST!!!!'.format(message)
                await client.send_message(message.channel, msg)
            else:
                msg = 'but but but but... MY DAD IS A COMPUTER!!!'.format(message)
                await client.send_message(message.channel, msg)
                
        if "ping" in message.content:
            msg = 'beebaobeebao'.format(message)
            await client.send_message(message.channel, msg)


        if "shit" in message.content:
            msg = 'pooopooo'.format(message)
            await client.send_message(message.channel, msg)

        if "poop" in message.content:
            msg = 'pp'.format(message)
            await client.send_message(message.channel, msg)

        if "arch" in message.content:
            msg = 'someone said arch?'.format(message)
            await client.send_message(message.channel, msg)

        if "kill -9" in message.content:
            msg = 'Ah {0.author.mention} killed me'.format(message)
            await client.send_message(message.channel, msg)
            pause = True
            
        if str(message.author) == "SpookyPotato#5306":
            msg = 'Pay attention in OS!'.format(message)
            await client.send_message(message.channel, msg)
            
        if str(message.author) == "hcai#6639":
            msg = 'beebao beebao'.format(message)
            await client.send_message(message.channel, msg)

        if str(message.author) == "stevenim#9159":
            msg = 'no u'.format(message)
            await client.send_message(message.channel, msg)

        if str(message.author) == "rudyghill#7321":
            msg = 'by the way'.format(message)
            await client.send_message(message.channel, msg)
           

        
@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "1\u1F4A9":
        msg = "poopoo".format(message)
        await client.send_message(message.channel, msg)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@bot.command(pass_context=True)
async def unkill(ctx):
    global pause
    pause = False
    await bot.say("Ah not dead anymore")





client.run(TOKEN)
