import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import subprocess

TOKEN = 'NjIzMjM3OTk4NTI3NjQzNzEx.XX_hng.GvnAc1qEKcv0cTHwBjYbJ5XU1fU'
pause = False

#client = discord.Client()


# example from github.com/Rapptz/discord.py/blob/examples/basic_voice.py
class Sad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """joins a voice channel"""
        

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    @commands.command()
    async def play(self, ctx, *, query):
        """play a file from local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('player error: %s' % e) if e else None)

        await ctx.send('Now Playing: {}'.format(query))

    @commands.command()
    async def stop(self, ctx):
        """stops and disconnects"""
        await ctx.voice_client.disconnect()



    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Your arent connected to a voice channel")
                raise commands.CommandError("Author is not connected to a voice channel")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


            



bot = commands.Bot(command_prefix=commands.when_mentioned_or("#"), description='big sad')




@bot.event
async def on_message(message):
    #print(message.content)
    #print(type(message.content))

    global pause


    if "unkill" in message.content:
        pause = False
        msg = 'Ah not dead anymore'.format(message)
        await message.channel.send(msg)
           

    
    if not pause:

        # we do not want the bot to reply to itself
        if message.author == bot.user:
            return

        if "steven" in message.content.lower():
            msg = 'Hello {0.author.mention}, Im StevenIm'.format(message)
            await message.channel.send(msg)

        if "but" in message.content.lower():     
            if "ping" in message.content:
                msg = 'but but but but... {0.author.mention} IS RACIST!!!!'.format(message)
                await message.channel.send(msg)
            else:
                msg = 'but but but but... MY DAD IS A COMPUTER!!!'.format(message)
                await message.channel.send(msg)
                
        if "ping" in message.content.lower():
            msg = 'beebaobeebao'.format(message)
            await message.channel.send(msg)


        if "shit" in message.content.lower():
            msg = 'pooopooo'.format(message)
            await message.channel.send(msg)

        if "poop" in message.content.lower():
            msg = 'pp'.format(message)
            await message.channel.send(msg)

        if "arch" in message.content.lower():
            msg = 'someone said arch?'.format(message)
            await message.channel.send(msg)

        if "fuck" in message.content.lower():
            msg = 'no u'.format(message)
            await message.channel.send(msg)

        if "kill -9" in message.content.lower():
            msg = 'Ah {0.author.mention} killed me'.format(message)
            await message.channel.send(msg)
            pause = True
            
        if ("how are you" in message.content.lower()) or ("how are u" in message.content.lower()):
            res = subprocess.run(['sensors','-f'], stdout=subprocess.PIPE)
            msg = res.stdout.decode('utf-8').strip()
            msg = msg.replace(" ","")
            begin = msg.find("+")
            end = msg.find("F")
            temp_str = msg[begin:end+1]
            send_msg = "Hi {0.author.mention}, im at {1} rn. Pretty sure im having a minor fever. thanks for asking tho.".format(message, temp_str)
            await message.channel.send(send_msg)

        
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "1\u1F4A9":
        msg = "poopoo".format(message)
        await message.channel.send(msg)



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


#@bot.command(pass_context=True)
#async def unkill(ctx):
#    global pause
#    pause = False
#    await ctx.send("Ah not dead anymore")

#@bot.command()
#async def report(ctx):
#    await ctx.send("hello")
#    res = subprocess.run(['ls','-l'], stdout=subprocess.PIPE)
#    await ctx.send(res.stdout.decode('utf-8'))


bot.add_cog(Sad(bot))


bot.run(TOKEN)




























