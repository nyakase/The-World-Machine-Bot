from interactions import *
import bot_data.generate_text as generate_text
import bot_data.dialogue_generator as dialogue_generator
import aiohttp
import aiofiles
from bot_data.error_handler import on_error
from interactions.ext.database.database import Database
from uuid import uuid4
import os

import textwrap

import nltk
nltk.download('punkt')

import pandas as pd
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import requests

from LeXmo import LeXmo

class Command(Extension):
    
    @extension_listener
    async def on_start(self):
        await Database.create_database('the bot remembers', Database.DatabaseType.USER, {'last_thing_said' : 'Hello.'}, True)
    
    @extension_command(description = 'Ask The World Machine a question.')
    @option(description='The question to ask!')
    async def ask(self, ctx : CommandContext, question : str):
        
        c = question[len(question) - 1]
        
        q = question + '?'
        
        embed = Embed(color=0x7d00b8)
        
        embed.set_author(
            name = f'"{question}"',
            icon_url= ctx.author.user.avatar_url
        )
        
        # * first stage...
        embed.description = '[ Thinking about what you have asked... <a:loading:1026539890382483576> ]'
        
        msg = await ctx.send(embeds = embed)
        
        result_ : str = await generate_text.GenerateText(q, ctx.author.user.username, 'gay gay homosexual gay')
        result_ = result_.strip()
        result_ = result_.strip('"')
        
        # * second stage...
        embed.description = '[ Judging your decisions... <a:loading:1026539890382483576> ]'
        
        await msg.edit(embeds=embed)
        
        result = LeXmo.LeXmo(result_)
        result.pop('text', None)
        
        
        emotion = max(result, key=result.get)
        
        
        twm = ''
        
        if emotion == 'anger':
            twm = 'https://cdn.discordapp.com/emojis/1023573452944322560.webp?size=96&quality=lossless'
        if emotion == 'anticipation':
            twm = 'https://cdn.discordapp.com/emojis/1023573456664662066.webp?size=96&quality=lossless'
        if emotion == 'disgust':
            twm = 'https://cdn.discordapp.com/emojis/1023573452944322560.webp?size=96&quality=lossless'
        if emotion == 'fear':
            twm = 'https://cdn.discordapp.com/emojis/1023573454307463338.webp?size=96&quality=lossless'
        if emotion == 'joy':
            twm = 'https://cdn.discordapp.com/emojis/1023573458296246333.webp?size=96&quality=lossless'
        if emotion == 'negative':
            twm = 'https://cdn.discordapp.com/emojis/1023573456664662066.webp?size=96&quality=lossless'
        if emotion == 'positive':
            twm = 'https://cdn.discordapp.com/emojis/1023573459676172359.webp?size=96&quality=lossless'
        if emotion == 'sadness':
            twm = 'https://cdn.discordapp.com/emojis/1023573454307463338.webp?size=96&quality=lossless'
        if emotion == 'surprise':
            twm = 'https://cdn.discordapp.com/emojis/1023573458296246333.webp?size=96&quality=lossless'
        if emotion == 'trust':
            twm = 'https://cdn.discordapp.com/emojis/1023573459676172359.webp?size=96&quality=lossless'
        
        # * third stage...
        embed.description = '[ Final decisions... <a:loading:1026539890382483576> ]'
        
        await msg.edit(embeds=embed)
        
        result_ = result_.replace('\n', ' ')
        
        n = 165
        r = ">".join(textwrap.wrap(result_, n, max_lines=4))
        finalresult_ = r.split('>')
        
        print(len(finalresult_))
        
        embed.description = ''
        
        await msg.edit(embeds=embed)
        
        uuid = uuid4()
        
        uuid = str(uuid)
        
        i = 0
        for text in finalresult_:
            
            if i < 5:
                if text == ' ' or text == '':
                    continue
                
                text = text.strip(' ')
                if not i == 0:
                    text = '...' + text
                
                await dialogue_generator.test(f'[{text}]', twm, uuid)
                
                file = File(f'Images/{uuid}.png', description=text)
                
                await ctx.channel.send(files = file)
            else:
                
                await ctx.channel.send('[ Message cut off for being too long. ]')
                break
            
            i += 1
            
        os.remove(f'Images/{uuid}.png')
        
    @ask.error
    async def you_fucked_up_gpt_three(self, ctx : CommandContext, error):
        
        embed = await on_error(error)
        
        await ctx.send(embeds= embed)
        
def setup(client):
    Command(client)