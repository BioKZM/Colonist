import discord
from discord.ext import commands
from main import embedColor

class Help(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def yardım(self,ctx):
        embed = discord.Embed(title="Yardım komutları",description="\n",color=embedColor)
        embed.add_field(name="!yardım `[ !help, !komutlar ]`",value="Bot üzerinde bulunan mevcut komutları görüntülemenizi sağlar.",inline=False)
        embed.add_field(name="!seviye `[ !level ]`",value="Mevcut ve gelecek seviye değerlerini gösteririr.",inline=False)
        embed.add_field(name="!sıralama `[ !rank ]`",value="Güncel liderlik tablosunu gösterir.",inline=False)
        embed.add_field(name="!bilgi",value="Sunucu hakkında detaylı bilgi almanı sağlar.",inline=False)
        embed.add_field(name="!mesajsil",value="En son attığın bilgi mesajını silmeni sağlar.",inline=False)
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))