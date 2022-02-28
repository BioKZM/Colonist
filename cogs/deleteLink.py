import discord
import json
import datetime
from discord.ext import commands
# from cogs.personalPoint import PersonalPoint
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashContext,cog_ext
from main import guildID


class DeleteLink(commands.Cog):
    def __init__(self,client):
        self.client = client

    @cog_ext.cog_slash(
        name = "linksil",
        description = "Linklerin yerleştirildiği mesajı düzenlemek için kullan.",
        guild_ids = guildID,
        options=[
            create_option(
                name = "id",
                description = "Silmek istediğin linkin ID'sini gir.",
                option_type = 3,
                required = True
            )
        ]
    )
    async def linksil(self,ctx:SlashContext,id):
        with open("files/linkEmbed.json") as file:
            data = json.load(file)

        del data[id]

        with open("files/linkEmbed.json","w") as file:
            json.dump(data,file,indent=4)
        
        description = ""
        for id in data:
            control = 0
            for value in data[f"{id}"]:
                control += 1
                if control == 2:
                    description += data[f"{id}"][f"{value}"]
                else:
                    description += data[f"{id}"][f"{value}"]+" "
            description+="\n"


        with open("files/linkDescription.py","w") as file:
            file.write('description = """')
            file.write(description)
            file.write('"""')

        await ctx.send("İşlem başarılı!")
        
        embed = discord.Embed(title = "Sosyal Medya Linkleri",description="Aşağıda bulunan linklere tıklayarak, sosyal medya hesaplarımıza ulaşabilirsin!\n\n"+description)
        

        embed.set_footer(text="Mars Game Colony",icon_url="https://i.hizliresim.com/k2dzgfw.jpg")
        embed.timestamp = datetime.now()
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

def setup(client):
	client.add_cog(DeleteLink(client))