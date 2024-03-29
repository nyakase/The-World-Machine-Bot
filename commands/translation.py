from interactions import *
from bot_data.error_handler import on_error
import bot_data.generate_text as text
from bot_data.embed_gen import fancy_send

class Command(Extension):
    
    @extension_message_command(name = '💡 Translate...')
    async def translate(self, ctx : CommandContext):
        
        await ctx.defer(ephemeral=True)
        
        lines = []
        
        with open('Languages.txt', 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
            
        select_options = []
            
        for line in lines:
            
            l = line.split(' - ')
            
            l = l[0]
            
            select_options.append(SelectOption(label=line, value=l))
            
        selectmenu = SelectMenu(custom_id= 'sus', placeholder= 'What language?', options=select_options)
        
        await ctx.send(components = selectmenu)
        
        button_ctx = await self.client.wait_for_component(selectmenu)
        
        msg = await fancy_send(button_ctx, '[ Translating message... <a:loading:1026539890382483576> ]', color = 0x2f3136)
        
        target_language = button_ctx.data.values[0]
        
        message = text.Response(f'Translate this message to {target_language} with new lines intact: "{ctx.target.content}".')
        message = message.strip('\n')
        message = message.strip('"')
        
        embed = Embed(
            title = f'Translation to {target_language}.',
            description= f'<:george_translation:1064601896297447544> ```{message}```',
            color=0x8100bf
        )
        
        embed.set_footer(f'Requested by {ctx.author.user.username}.', icon_url= ctx.author.user.avatar_url)

        await ctx.target.reply(embeds=embed)
        
        await msg.delete()
    
    @translate.error
    async def error(self, ctx : CommandContext, error):
        
        embed = await on_error(error)
        
        await ctx.send(embeds=embed)
        
def setup(client):
    Command(client)