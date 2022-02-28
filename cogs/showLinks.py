import discord
import json
from datetime import datetime
from discord.ext import commands
from main import embedColor

class Link(commands.Cog):
    def __init__(self,client):
        self.client = client

    
    @commands.command()
    async def link(ctx):
        with open("files/linkEmbed.json") as file:
            data = json.load(file)

        description = "\n"
        for id in data:
            control = 0
            for value in data[f"{id}"]:
                control += 1
                if control == 2:
                    description += data[f"{id}"][f"{value}"]
                else:
                    description += data[f"{id}"][f"{value}"]+" "
            description+="\n"
            
        embed = discord.Embed(title = "Sosyal Medya Linkleri",description="Aşağıda bulunan linklere tıklayarak, sosyal medya hesaplarımıza ulaşabilirsin!\n\n"+description,color=embedColor)
        embed.set_footer(text="Mars Game Colony",icon_url="https://i.hizliresim.com/k2dzgfw.jpg")
        embed.timestamp = datetime.now()
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Link(client))