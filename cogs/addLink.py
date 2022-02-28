import discord
import json
import datetime
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option
from discord_slash import SlashContext,cog_ext
from main import guildID

class AddLink(commands.Cog):
    def __init__(self,client):
        self.client = client

    @cog_ext.cog_slash(
        name = "linkekle",
        description = "Linklerin gösterildiği mesajı düzenlemek için kullan.",
        guild_ids = guildID,
        options=[
            create_option(
                name = "id",
                description = "Gireceğin linkin ID'sini gir.",
                option_type = 4,
                required=True,
            ),
            create_option(
                name = "emoji",
                description = "Bir emoji gir.",
                option_type=3,
                required=True,
            ),
            create_option(
                name = "platform_ismi",
                description = "Linki paylaşmak istediğin sosyal medya adresini tanıtmak için bir isim gir.",
                option_type=3,
                required=True,
            ),
            create_option(
                name = "link",
                description = "Sosyal medyanın linkini gir.",
                option_type=3,
                required=True,
            )
        ]
    )
    async def linkEkle(ctx:SlashContext,id,emoji,platform_ismi,link):
        with open("files/linkEmbed.json") as file:
            data = json.load(file)
        
        data[f"{id}"] = {
            "emoji" : str(emoji),
            "sosyal_medya" : "["+platform_ismi+"]",
            "link" : "("+link+")"
        }
        
        with open("files/linkEmbed.json","w") as file:
            json.dump(data,file,indent=4)
            
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

        with open("files/linkDescription.py","w") as file:
            file.write('description = """ ')
            file.write(description)
            file.write('"""')
            file.close()
        
        await ctx.send("İşlem başarılı!")
        
        embed = discord.Embed(title = "Sosyal Medya Linkleri",description="Aşağıda bulunan linklere tıklayarak, sosyal medya hesaplarımıza ulaşabilirsin!\n"+description)
        

        embed.set_footer(text="Mars Game Colony",icon_url="https://i.hizliresim.com/k2dzgfw.jpg")
        embed.timestamp = datetime.now()
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(AddLink(client))