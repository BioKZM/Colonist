import discord
from discord.ext import commands
from functions.userClass import User

def getSortedMembers(ctx):
	di = {}
	for member in ctx.guild.members:
		user = User(member.id)
		memberName_ = f"{member.display_name}   /   [ {member.name} ]"
		if not member.bot:
			di[memberName_] = [user.XP,user.levelName]
			sortedMembers = dict(sorted(di.items(),key=lambda item:item[1],reverse=True))
		else:
			pass
	return sortedMembers

class Rank(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases=["rank"])
    async def sıralama(self,ctx):
        sortedMembers = getSortedMembers(ctx)
    
        embed=discord.Embed(title="Sıralama",inline=False,color=0x8d42f5)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        count = 1

        for key,value in sortedMembers.items():
            embed.add_field(name="{} - {}".format(count,key),value="**Puan**: {}\n**Rütbe**: {}".format(value[0],value[1]),inline=False)
            count += 1
            if count == 11:break

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Rank(client))