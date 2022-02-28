import asyncio
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def clear(self,ctx,amount=1):
        if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
            await ctx.channel.purge(limit=amount+1)
            await ctx.channel.send("{} mesaj silindi! ✅".format(amount))
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=1)
        else:
            await ctx.channel.send("Bu komutu kullanmaya izniniz yok!")


def setup(client):
    client.add_cog(Clear(client))