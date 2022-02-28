import discord
from discord.utils import get
from discord.ext import commands
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashContext, cog_ext
from main import guildID
from functions.userClass import User



class AddPointToSpaceShip(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.platformXPs = {
    		"PC":10000,
    		"Mobil":5000,
    		"Hypercasual":2000,
    		"GameJam":1000
        	}

    def __addPointToSpaceShip(self,members,platform,shipRole):
        for member in members:
            if shipRole in member.roles:
                user = User(member.id)
                user.addXP(self.platformXPs[platform])
    @cog_ext.cog_slash(
        name = "gemipuan",
        description = "Kullanıcılar ekstra puan vermek için kullan!",
        guild_ids = guildID,
        options = [
            create_option(
                name = "gemi",
                description = "Bir gemi seç!",
                option_type = 8,
                required = True,
            ),
            create_option(
                name = "platform",
                description = "Seçilen platforma göre puan ver",
                option_type = 3,
                required = True,
                choices = [
                    create_choice(
                        name = "PC",
                        value = "PC",
                    ),
                    create_choice(
                        name = "Mobil",
                        value = "Mobil",
                    ),
                    create_choice(
                        name = "Hypercasual",
                        value = "Hypercasual",
                    ),
                    create_choice(
                        name = "GameJam",
                        value = "GameJam",
                    )
                ]
            )
        ]
    )
    async def _gemipuan(self,ctx:SlashContext,platform:str,gemi:str):
        if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
            shipRole = get(ctx.guild.roles,name=str(gemi))
            self.__addPointToSpaceShip(ctx.guild.members,platform,shipRole)
            embed = discord.Embed(title="Puan Artışı",description = f"**{shipRole.mention}** adlı geminin mürettebatına **{self.platformXPs[platform]}** puan eklendi!")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(AddPointToSpaceShip(client))