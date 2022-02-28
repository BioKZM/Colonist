import discord
import json
from discord.ext import commands
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashContext,cog_ext
from main import guildID, embedColor

def changeModifier(modifier,value):
	with open("userFiles/modifier.json") as file:
		data = json.load(file)

	data[modifier] = value
	
	with open("userFiles/modifier.json","w") as file:
		json.dump(data,file,indent = 4)

class Modifier(commands.Cog):
	def __init__(self,client):
		self.client = client

	@cog_ext.cog_slash(
		name="çarpan",
		description="Bir çarpan değeri gir!",
		guild_ids=guildID,
		options=[
			create_option(
				name="çarpan_tipi",
				description="Değiştirmek istediğin çarpan değerini seç!",
				option_type=3,
				required=True,
				choices=[
					create_choice(
						name="Kamera Çarpanı",
						value="Kamera",
					),
					create_choice(
						name="Yayın Çarpanı",
						value="Yayın"
					),
					create_choice(
						name="Dakika Çarpanı",
						value="Dakika"
					)
				]
			),
			create_option(
				name="çarpan",
				description="Çarpan değerini değiştir!",
				option_type=4,
				required=True,
			)

		]
	)
	async def _çarpan(self,ctx:SlashContext,çarpan:int,çarpan_tipi:str):
		if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
			changeModifier(çarpan_tipi,çarpan)
			embed = discord.Embed(
				title = "Çarpan değişimi",
				description = f"{çarpan_tipi} çarpanı şu değere değiştirildi = **{çarpan}**,",	
				color = embedColor
			)
			await ctx.send(embed=embed)
		else:
			await ctx.send("Bu komutu kullanmaya izniniz yok!")


def setup(client):
	client.add_cog(Modifier(client))