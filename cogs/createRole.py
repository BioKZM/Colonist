import discord 
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext
from main import guildID
from discord.utils import get


class CreateRole(commands.Cog):
    def __init__(self,client):
        self.client = client

    @cog_ext.cog_slash(
        name = "rololuştur",
        description="Bir rol oluşturmak için kullan!",
        guild_ids=guildID,
        options=[
            create_option(
                name="rol",
                description="Bir rol ismi belirle.",
                option_type=3,
                required=True
            ),
            create_option(
                name="emoji",
                description="Bir emoji belirle.",
                option_type=3,
                required=True
            )
        ]
    )
    async def createRole(self,ctx,rol,emoji):
        guild = ctx.guild
        roleName = f"{rol} {emoji}"
        await guild.create_role(name=roleName)
        role = get(guild.roles,name=roleName)
        await ctx.send(embed=discord.Embed(title="Rol oluşturma işlemi",description=f"{role.mention} rolü oluşturuldu."))

def setup(client):
    client.add_cog(CreateRole(client))