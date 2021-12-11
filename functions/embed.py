import asyncio
import discord  

def botEmbed(guild,bot,description,title="",footer="",icon=False):
    botColor = discord.utils.get(guild.members, id=bot.user.id).color
    if title == "":
        title = guild.name
    embed = discord.Embed(title=title, description=description, color=botColor)
    
    if icon:
        embed.set_thumbnail(url=guild.icon_url)
    if footer!="":
        embed.set_footer(text=footer)
    return embed