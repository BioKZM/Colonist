import discord
import json
from discord.ext import commands
from discord.utils import get
# from cogs.personalPoint import PersonalPoint
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashContext,cog_ext
from main import guildID


async def createChannel(ctx,name,category,topic=None):
	guild = ctx.guild
	await guild.create_text_channel(name=name,category=category,topic=topic)

async def createVC(ctx,name,category):
	guild = ctx.guild
	await guild.create_voice_channel(name=name,category=category)

class CreateSpaceShip(commands.Cog):
    def __init__(self,client):
        self.client = client


    @cog_ext.cog_slash(
        name="gemiyap",
        description="Bir gemi oluşturmak için kullan!",
        guild_ids=guildID,
        options=[
            create_option(
                name="gemi",
                description="Gemi ismini gir.",
                option_type=3,
                required=True,
            )
        ]
    )
    async def _createSpaceShip(self,ctx:SlashContext,gemi):
        guild = ctx.guild
        await guild.create_role(name=f"🚀{gemi}")
        await guild.create_role(name=f"🚀{gemi} - Captain")
        unit = get(guild.roles,name="Unit")
        shipRole = get(guild.roles,name=f"🚀{gemi}")
        captain = get(guild.roles,name=f"🚀{gemi} - Captain")
        engineer = get(guild.roles,name = "The Engineer")
        embed = discord.Embed(
            title = "Gemi Oluşturma İşlemi",
            description = f"{shipRole.mention} gemisi oluşturuluyor",
            color = 0x8d42f5
        )
        embedMessage = await ctx.send(embed=embed)
        overwrites = {
            ctx.guild.default_role : discord.PermissionOverwrite(
                view_channel=False
            ),
            unit : discord.PermissionOverwrite(
                add_reactions=True,
                view_channel=True,
                read_message_history=True,
                read_messages=True,
                send_messages=False,
                speak=False,
                stream=False,
                connect=True,
                ),
            shipRole : discord.PermissionOverwrite(
                add_reactions=True,
                attach_files=True,
                connect=True,
                deafen_members=True,
                embed_links=True,
                external_emojis=True,
                move_members=True,
                mute_members=True,
                read_message_history=True,
                read_messages=True,
                send_messages=True,
                speak=True,
                stream=True,
                use_external_emojis=True,
                view_channel=True,
                ),
            captain : discord.PermissionOverwrite(
                add_reactions=True,
                attach_files=True,
                connect=True,
                deafen_members=True,
                embed_links=True,
                external_emojis=True,
                manage_channels=True,
                move_members=True,
                mute_members=True,
                read_message_history=True,
                read_messages=True,
                send_messages=True,
                speak=True,
                stream=True,
                use_external_emojis=True,
                view_channel=True,
            ),
            engineer : discord.PermissionOverwrite(
                add_reactions=True,
                attach_files=True,
                connect=True,
                deafen_members=True,
                embed_links=True,
                external_emojis=True,
                manage_channels=True,
                move_members=True,
                mute_members=True,
                read_message_history=True,
                read_messages=True,
                send_messages=True,
                speak=True,
                stream=True,
                use_external_emojis=True,
                view_channel=True,
            )
        }
        category = await ctx.guild.create_category_channel(name=f"🚀{gemi}",overwrites=overwrites)
        await createChannel(ctx,f"🚀{gemi}-hall",category,"Uçuşa geçmeden önce, mürettebata yön verecek kaptanın seçildiği oda.")
        await createChannel(ctx,"📓captain-s-logbook",category,"Kaptanın, Mars yolculuğunda, yaşadığı tecrübeleri kaydettiği günlüğün bulunduğu oda")
        await createChannel(ctx,"💬chat-box",category,"Mürettebatın özgürce sohbet edebileceği oda.")
        await createChannel(ctx,"🧠brai̇nstorm-notes",category,"Mürettebatın Mars yolculuğu sırasında, ilham aldıkları ve keşfettikleri fikirleri tuttukları oda.")
        await createChannel(ctx,"📋checklist",category,"Mürettebatın, yolculuk sırasında gerçekleştirecekleri dönüm noktalarını yazdıkları oda")
        await createChannel(ctx,"🔗reference-archive",category,"Geminin kütüphanesi")
        await createChannel(ctx,"📜documents",category,"Gemi kütüphanesi 2.kat")
        await createChannel(ctx,"🎨visual-arts",category,"Gemi kütüphanesi 3.kat")
        await createChannel(ctx,"🎹sound-arts",category,"Gemi kütüphanesi 4.kat")

        await createVC(ctx,"🟥 Red Room",category)
        await createVC(ctx,"⬛ Black Room",category)
        await createVC(ctx,"🟩 Green Room",category)


        ship = str(f"🚀{gemi}").lower()
        captainsHall = get(guild.channels,name=f"{ship}-hall")

        with open("files/captainHalls.json") as file:
            captainHalls = json.load(file)
            captainHalls[gemi] = (captainsHall.id)
            
        message = await captainsHall.send("**Geminin kaptanını** belirlemek için, **kaptan** olacak kişinin aşağıdaki emojiye basması gerekmektedir.\n**Uyarı**, bu **tek seferlik** bir seçim olduğu için, tıklamadan önce **iyice karar vermeniz** tavsiye edilir.")

        await message.add_reaction("🚀")
        

        with open("files/captainHalls.json","w") as file:
            json.dump(captainHalls,file,indent=4)
            
        embed = discord.Embed(
            title = "Gemi Oluşturma İşlemi",
            description = f"{shipRole.mention} gemisi oluşturuldu. Katılacak mürettebatın dikkatine!",color=0x8d42f5
        )
        await embedMessage.edit(embed=embed)

def setup(client):
    client.add_cog(CreateSpaceShip(client))