import asyncio

import discord
import youtube_dl
from urllib.parse import quote
from discord.ext import commands

import subprocess
import re
import random


# read token
f = open('token','r')
TOKEN = str(f.readline())
f.close()
BOT_PREFIX = "%"

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

tts_lang = {
    'afrikaans'     :   'af',
    'irish'         :   'ga',
    'albanian'      :   'sq',
    'italian'       :   'it',
    'arabic'        :   'ar',
    'japanese'      :   'ja',
    'azerbaijani'   :   'az',
    'kannada'       :   'kn',
    'basque'        :   'eu',
    'korean'        :   'ko',
    'bengali'       :   'bn',
    'latin'         :   'la',
    'belarusian'    :   'be',
    'latvian'       :   'lv',
    'bulgarian'     :   'bg',
    'lithuanian'    :   'lt',
    'catalan'       :   'ca',
    'macedonian'    :   'mk',
    'chinese simplified'    :   'zh-CN',
    'malay'         :   'ms',
    'chinese traditional'   :   'zh-TW',
    'maltese'       :   'mt',
    'croatian'      :   'hr',
    'norwegian'     :   'no',
    'czech'         :   'cs',
    'persian'       :   'fa',
    'danish'        :   'da',
    'polish'        :   'pl',
    'dutch'         :   'nl',
    'portuguese'    :   'pt',
    'english'       :   'en',
    'romanian'      :   'ro',
    'esperanto'     :   'eo',
    'russian'       :   'ru',
    'estonian'      :   'et',
    'serbian'       :   'sr',
    'filipino'      :   'tl',
    'slovak'        :   'sk',
    'finnish'       :   'fi',
    'slovenian'     :   'sl',
    'french'        :   'fr',
    'spanish'       :   'es',
    'galician'      :   'gl',
    'swahili'       :   'sw',
    'georgian'      :   'ka',
    'swedish'       :   'sv',
    'german'        :   'de',
    'tamil'         :   'ta',
    'greek'         :   'el',
    'telugu'        :   'te',
    'gujarati'      :   'gu',
    'thai'          :   'th',
    'haitian creole':   'ht',
    'turkish'       :   'tr',
    'hebrew'        :   'iw',
    'ukrainian'     :   'uk',
    'hindi'         :   'hi',
    'urdu'          :   'ur',
    'hungarian'     :   'hu',
    'vietnamese'    :   'vi',
    'icelandic'     :   'is',
    'welsh'         :   'cy',
    'indonesian'    :   'id',
    'yiddish'       :   'yi'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

pause = False
yoshi_unlock = False

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.tts_lang_sel = 'en'
        self.is_speaking = False
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(aliases=['p','pl','pla'])
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        
        
        #ffaudio = discord.FFmpegPCMAudio('res/'+query, stderr=subprocess.PIPE)
        #err = ffaudio.stderr.decode('utf-8')

        #if(err != None):
        #    ctx.send('bro i literarily physically can\'t say ***{}***'.format(query))


        ffaudio = discord.FFmpegPCMAudio('res/'+query)
        source = discord.PCMVolumeTransformer(ffaudio)


        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('***{}***'.format(query))

    @commands.command()
    async def ytdlp(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('***{}***'.format(player.title))

    @commands.command(aliases=['y'])
    async def yt(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('***{}***'.format(player.title))
   

    
    def speak_after_callback(self, e):
        if e:
            print('Player error %s' % e)
        print("ENTERED CALLLLBACK")
        self.is_speaking = False


    @commands.command(aliases=['l'])
    async def lang(self, ctx, *, lang_key):
        if lang_key not in tts_lang:
            await ctx.send(f"i physically can\'t speak {lang_key}")
        else:
            self.tts_lang_sel = tts_lang[lang_key]
            await ctx.send(f"i speak {lang_key} bitchass")
        pass
    @commands.command(aliases=['s'])
    async def speak(self, ctx, *, query):
        """Use google translate request a wav download to local and playback and delete, the max we can have is 264 after padding"""
        query_parse = quote(query)
        async with ctx.typing():
            """Download Audio from google translate"""
            if(len(query_parse) > 264):
                exceed = len(query_parse) - 264
                await ctx.send(f"shit is too long give me tldr {exceed} less")
            else:
                self.is_speaking = True # lock
                res = subprocess.run(["wget","-O","res/tmp","-U","mozilla","https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q="+query_parse+"&tl="+self.tts_lang_sel], stdout=subprocess.PIPE)
                """Playback the downloaded audio to the voice channel"""
                ffaudio = discord.FFmpegPCMAudio('res/tmp')
                source = discord.PCMVolumeTransformer(ffaudio)
                ctx.voice_client.play(source, after=self.speak_after_callback)
                while(self.is_speaking):
                    pass # we wait until speak_after_callback is called (audio finish playing)
                """Clean up the downloaded audio file"""
                #res = subprocess.run(["rm","res/tmp"])
            pass
        pass
    @commands.command(aliases=['ls'])
    async def long_speak(self, ctx, *, query):
        """We are trying to solve the google 264 byte query string length limit by dividing"""
        req_list = []
        count = 0
        sub_str = ""

        for c in query:  # it should work but those damn %20 and unbroken up words lol
            if(count == 244):
                req_list.append(sub_str)
                sub_str = ""
                count = 0
            else:
                sub_str += c
                if(c == ' ' or c == '\n'):
                    count += 3
                else:
                    count += 1
        req_list.append(sub_str)

        for req in req_list:
            await self.speak(ctx, query=req)




    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @ytdlp.before_invoke
    @speak.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or(BOT_PREFIX),
                   description='Relatively simple music bot example')









@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')




@bot.event
async def on_message(message):
    #print(message.content)
    #print(type(message.content))
    
    global pause
    global yoshi_unlock


    if "unkill" in message.content:
        pause = False
        msg = 'Ah not dead anymore'.format(message)
        await message.channel.send(msg)
           

    
    if not pause:

        if "--yoshi-unlock" == message.content.lower():
            yoshi_unlock = True
        if "--yoshi-lock" == message.content.lower():
            yoshi_unlock = False


        # we do not want the bot to reply to itself, or do we?
        if (message.author == bot.user):
            if (not yoshi_unlock):
                return
            else:     # start yooshi flood
                if "ooo" in message.content.lower():
                    msg = 'yo'
                    t = random.randint(2,30)
                    for i in range(t):
                        cap = random.randint(0,99)
                        if(cap < 50):
                            msg += 'o'
                        else:
                            msg += 'O'
                    msg += 'shi'
                    t = random.randint(2,15)
                    for i in range(t):
                        msg += 'i'

                    await message.channel.send(msg)

        
        

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
            msg = ':poop:'
            await message.channel.send(msg)

        if "arch" in message.content.lower():
            msg = 'someone said arch?'.format(message)
            await message.channel.send(msg)

        if "fuck" in message.content.lower():
            msg = 'no u'.format(message)
            await message.channel.send(msg)

        if "ooo" in message.content.lower():
            msg = 'yo'
            t = random.randint(2,30)
            for i in range(t):
                cap = random.randint(0,99)
                if(cap < 50):
                    msg += 'o'
                else:
                    msg += 'O'
            msg += 'shi'
            t = random.randint(2,15)
            for i in range(t):
                msg += 'i'

            await message.channel.send(msg)

        if "kill -9" == message.content.lower():
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
            temp = float(temp_str[1:-2])
            send_msg = "Hi {0.author.mention}, im at {1} rn. ".format(message, temp_str)

            if(temp >= 100):
                send_msg += "Pretty sure im having a minor fever rn :hot_face: thanks for asking tho"
            elif(temp < 100):
                send_msg += "Just chillin :cool:"
            
            await message.channel.send(send_msg)
        
        
        if "test" == message.content.lower():
            
            pass






        await bot.process_commands(message)





@bot.command()
async def list(ctx):
    res = subprocess.run(['ls', 'res/'], stdout=subprocess.PIPE)
    msg = res.stdout.decode('utf-8')
    await ctx.send("I would say:\n"+msg)



@bot.command()
async def test(ctx, input_str):
    
    pass
    




















bot.add_cog(Music(bot))
bot.run(TOKEN)









