from interactions import *
from bot_data.error_handler import on_error
from bot_data.embed_gen import fancy_send

class Command(Extension):
    
    @extension_command(description = 'Put Command Description here.')
    async def command_name(self, ctx : CommandContext):
        pass
    
    @command_name.error
    async def error(self, ctx : CommandContext, error):
        
        embed = await on_error(error)
        
        await ctx.send(embeds=embed)
        
def setup(client):
    Command(client)