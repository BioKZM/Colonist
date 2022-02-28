import discord
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option
from discord_slash import SlashContext,cog_ext
from main import guildID
from functions.userClass import User

class PersonalPoint(commands.Cog):
    def __init__(self,client):
        self.client = client

    @cog_ext.cog_slash(
        name = "kişiselpuan",
        description="Kişiye özel puan vermek için kullan!",
        guild_ids=guildID,
        options=[
            create_option(
                name = "kullanıcı",
                description="Bir kullanıcı seç!",
                option_type=6,
                required=True,
            ),
            create_option(
                name="puan",
                description="Bir puan değeri gir!",
                option_type=4,
                required=True,
            )
        ]
    )
    async def _kişiselpuan(self,ctx:SlashContext,kullanıcı:discord.Member,puan:int):
        if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
            user = User(kullanıcı.id)
            user.addXP(puan)
            
            embed=discord.Embed(title="Puan ekleme işlemi",description=f"**{kullanıcı.name}** adlı kullanıcıya **{puan}** puan eklendi!",color=kullanıcı.top_role.color)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Bu komutu kullanmaya izniniz yok!")


def setup(client):
    client.add_cog(PersonalPoint(client))