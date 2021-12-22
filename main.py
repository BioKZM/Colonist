import discord
import os
# import sys
import asyncio
import random
from discord.ext import commands,tasks
from discord.utils import get
from keep_alive import keep_alive
from discord_ui import UI,Button,ButtonStyle
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
# from Files.levels import nextXP, nextLevel
from discord import ChannelType
from firebase import firebase
# from functions.embed import botEmbed
from functions.classes import User,experiences,levelNames
from files.embedDictionary import dictionary
from files.openShips import captainHalls
from files.infoMessage import info


TOKEN = os.environ['TOKEN']
serverURL = os.environ['serverURL']


keep_alive()
firebase = firebase.FirebaseApplication(serverURL,None)
client = commands.Bot(command_prefix=['!','-'], intents=discord.Intents.all(),help_command=None,case_insensitive=True)
intents = discord.Intents.all()
intents.members = True
ui = UI(client)
slash = SlashCommand(client,sync_commands=True)
guildID = [888759899226538025]




@client.event
async def on_ready():
	print("On Mars Way!")
	await client.change_presence(status=discord.Status.online,activity=discord.Game("🚀 On My Way To Mars!"))


@client.event
async def on_member_join(member):
	guild = client.guilds[0]
	channel = client.get_channel(915299360202448978)
	await member.edit(nick="👁 WATCHER")
	role = get(guild.roles,name="Unit")
	role2 = get(guild.roles,name="Guest")
	await member.add_roles(role)
	await member.add_roles(role2)
	await channel.send(f"**{member.name}** ({member.mention}) sunucuya iniş yaptı! Hoşgeldin!")
	user = User(member.id)

@client.event
async def on_message(message):
	channel = str(message.channel)
	memberID = message.author.id
	if not message.author.bot:
		user = User(memberID)
		if channel == "kendini-tanıt":
			if user.boolMessage == True:
				user.addXP(250)
				user.update('boolMessage','False')
				channel = client.get_channel(id=910547555245494322)
				await channel.send(f"<@{memberID}>,<#901248994922098718> kanalında kendinizi tanıttığınız için **250 XP** kazandınız!")
			else:
				pass
	await client.process_commands(message)



@client.command(aliases=["help","komutlar"])
async def yardım(ctx):
	embed = discord.Embed(title="Yardım komutları",description="\n",color=0x8d42f5)
	embed.add_field(name="!yardım `[ !help, !komutlar ]`",value="Bot üzerinde bulunan mevcut komutları görüntülemenizi sağlar.",inline=False)
	embed.add_field(name="!seviye `[ !level ]`",value="Mevcut ve gelecek seviye değerlerini gösteririr.",inline=False)
	embed.add_field(name="!sıralama `[ !rank ]`",value="Güncel liderlik tablosunu gösterir.",inline=False)
	embed.add_field(name="!bilgi",value="Sunucu hakkında detaylı bilgi almanı sağlar.",inline=False)
	embed.add_field(name="!mesajsil",value="En son attığın bilgi mesajını silmeni sağlar.",inline=False)
	await ctx.channel.send(embed=embed)


def memberSituation(prev,cur):
	if prev.channel and cur.channel:
		if cur.self_stream and cur.self_video:
			return "stream + cam"
		if cur.self_stream:
			return "stream"
		if cur.self_video:
			return "cam"
		elif not cur.self_stream and not cur.self_video:
			return ""

	


@client.event
async def on_voice_state_update(member,prev,cur):
	if not member.bot:
		user = User(member.id)
		
		if memberSituation(prev,cur) == "stream":
			modifier = user.getModifier(location="Yayın Çarpanı")
			user.update("modifier",modifier)
			
		elif memberSituation(prev,cur) == "cam":
			modifier = user.getModifier(location="Kamera Çarpanı")
			user.update("modifier",modifier)
			
		elif memberSituation(prev,cur) == "stream + cam":
			camModifier = user.getModifier(location="Kamera Çarpanı")
			streamModifier = user.getModifier(location="Yayın Çarpanı")
			modifier = camModifier + streamModifier
			user.update("modifier",modifier)
			
		elif memberSituation(prev,cur) == "":
			modifier = user.getModifier(location="Dakika Çarpanı")
			user.update("modifier",modifier)
				
				


@tasks.loop(minutes=1)
async def voicech():
	guild = client.guilds[0]
	vcList = [channel.id for channel in client.get_all_channels() if channel.type==ChannelType.voice]
	for channelID in vcList:
		voicechannel = client.get_channel(channelID)
		members = voicechannel.members

		for member in members:
			if not member.bot:
				user = User(member.id)
				user.updateXP()
				if not user.haveMaxLevel():
					if user.XP >= user.currentLevelMaxXP:
						user.level = user.getLevel(user.XP)
						user.putLevel(user.level)
						user.levelName = levelNames[user.level-1]
						role = get(guild.roles, name=user.levelName)
						await member.add_roles(role)
						print(role)
						
						channel = client.get_channel(id=910547555245494322)
						await channel.send(f"Tebrikler <@{member.id}>! **{user.level}**. seviyeye ulaştın!")
						await asyncio.sleep(3)
		

@voicech.before_loop
async def before_voicech():
	await client.wait_until_ready()
	print("Channel Update Loop OK!")
voicech.start()

@client.event
async def on_raw_reaction_add(payload):
	channel = payload.channel_id
	member = payload.member
	reaction = payload.emoji
	guild = client.get_guild(payload.guild_id)

	if channel == 905888377071616090:
		if not member.bot:
			channel = get(guild.channels,id=channel)
			for emoji,role in dictionary.items():
				if str(reaction) == str(emoji):
					role = get(guild.roles,name=role)
					await member.add_roles(role)
	
	for gemi,id in captainHalls.items():
		if channel == id:
			if str(reaction) == "🚀":
				if not member.bot:
					role = get(guild.roles,name =f"{gemi} - Captain" )
					await member.add_roles(role)
					gemi = str(f"{gemi}").lower()
					channel = get(guild.channels,name=f"{gemi}-hall")
					await channel.delete()



@client.event
async def on_raw_reaction_remove(payload):
	channel = payload.channel_id
	guild = client.get_guild(payload.guild_id)
	member = guild.get_member(payload.user_id)
	reaction = payload.emoji
	if channel == 905888377071616090:
		if not member.bot:
			channel = get(guild.channels,id=channel)
			for emoji,role in dictionary.items():
				if str(reaction) == str(emoji):
					role = get(guild.roles,name=role)
					await member.remove_roles(role)



@client.command(aliases=["level"])
async def seviye(ctx,member:discord.Member=None):
	if member == None:
		member = ctx.author

	user = User(member.id)
	if not member.bot:
		if member.id == 276066808887508992:
			embed = discord.Embed(title=f"{member.name}#{member.discriminator} adlı ku½ll#n$cının de\4r½l%i",description="",color=0x8d42f5)
			embed.add_field(name="M#vc&-*/$ De¨eßrL3r - ❌",value="Seviyesi = **{}**\nPuanı = **-999999999999**\nRütbesi = **{}**".format("∞","undefined",inline=False))
			embed.add_field(name="B1r s0½rak` r#t!e - 🔒",value="Bir sonraki rütbe = **unknown**\n[_Hata] = **k[]ll4n1c1 v3R1lEri h4$arLI**",inline=False)
			embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
			message = await ctx.send(embed=embed)
			
			embed2 = discord.Embed(title="f adlı ku½ll#n$cının de\4r½l%i",description="",color=0x8d42f5)
			embed2.add_field(name="P4/7(+n De¨eßrL3r - ❌",value="Er0oR = **{}**\nRütbesi = **{}**\nMevcut = **{}**".format("√52734156","undefined",random.randint(-999999,999999)),inline=False)
			embed2.add_field(name="B'r s0½rak# r}£!æ - 🔒",value="H½3t_l| d3ğ½9oken = **unknown**\n[_Hata] = **k[u]ll4n1c1 v3R~|Eri hæ$ar/I**",inline=False)
			embed2.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
			for i in range(0,1000):
				numbers = [1,2,3]
				await asyncio.sleep(random.choice(numbers))
				await message.edit(embed=embed2)
				await asyncio.sleep(random.choice(numbers))
				await message.edit(embed=embed)
		async with ctx.typing():
			await asyncio.sleep(1)
			embed = discord.Embed(title=f"{member.name}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
			embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = **{}**\n Puanı = **{}**\n Rütbesi = **{}**\n".format(user.level,user.XP,user.levelName,inline=False))
			if user.haveMaxLevel():
				embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level-1])-user.XP}**" if not user.haveMaxLevel() else "Maksimum seviyeye ulaştınız!",inline=False)
			elif not user.haveMaxLevel():
				if experiences[user.level-1] - user.XP <= 0:
					embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.getLevel(user.XP)-1]}** rütbesine ulaştın! Seviye atlamak için ses kanalına girebilirsin.",inline=False)
				else:
					embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level-1])-user.XP}**",inline=False)

			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

			await ctx.send(embed=embed)



@client.command()
async def clear(ctx,amount=1):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		await ctx.channel.purge(limit=amount+1)
		await ctx.channel.send("{} mesaj silindi! ✅".format(amount))
		await asyncio.sleep(3)
		await ctx.channel.purge(limit=1)
	else:
		await ctx.channel.send("Bu komutu kullanmaya izniniz yok!")

def changeModifier(location,modifier):
	firebase.put(f"modifiers/{location} Çarpanı",'modifier',modifier)

@slash.slash(
	name="çarpan",
	description="Bir çarpan değeri gir!",
	guild_ids=guildID,
	options=[
		create_option(
			name="görüntü",
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
async def _çarpan(ctx:SlashContext,çarpan:int,görüntü:str):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		changeModifier(görüntü,çarpan)
		await ctx.send(embed=botEmbed(ctx.guild,client,f"{görüntü} çarpanı şu değere değiştirildi! = **{çarpan}**",f"{görüntü} çarpanı değişimi!"))
	else:
		await ctx.send("Bu komutu kullanmaya izniniz yok!")

def getSortedMembers(ctx):
	di = {}
	for member in ctx.guild.members:
		user = User(member.id)
		memberName_ = f"{member.display_name}   //   [ {member.name} ]"
		if not member.bot:
			di[memberName_] = [user.XP,user.levelName]
			sortedMembers = dict(sorted(di.items(),key=lambda item:item[1],reverse=True))
		else:
			pass
	return sortedMembers

@client.command(aliases=["rank"])
async def sıralama(ctx):
	async with ctx.typing():
		sortedMembers = getSortedMembers(ctx)
	
		embed=discord.Embed(title="Sıralama",inline=False,color=0x8d42f5)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

		count = 1

		for key,value in sortedMembers.items():
			embed.add_field(name="{} - {}".format(count,key),value="**Puan**: {}\n**Rütbe**: {}".format(value[0],value[1]),inline=False)
			count += 1
			if count == 11:break

		await ctx.send(embed=embed)


def __addPointToSpaceShip(members, platform, shipRole):
	for member in members:
		if shipRole in member.roles:
			user = User(member.id)
			user.addXP(platformXPs[platform])
platformXPs = {
		"PC":10000,
		"Mobil":5000,
		"Hypercasual":2000,
		"GameJam":1000
	}
@slash.slash(
	name="gemipuan",
	description = "Kullanıcılara ekstra puan vermek için kullan!",
	guild_ids=guildID,
	options=[
		create_option(
			name="gemi",
			description="Bir gemi seç!",
			option_type=8,
			required=True

		),
		create_option(
			name = "platform",
			description="Seçilen platforma göre puan ver",
			option_type=3,
			required=True,
			choices=[
				create_choice(
					name="PC",
					value="PC"
				),
				create_choice(
					name="Mobil",
					value="Mobil",
				),
				create_choice(
					name="Hypercasual",
					value="Hypercasual",
				),
				create_choice(
					name="GameJam",
					value="GameJam"
				)
			]
		)
	]
)
async def _gemipuan(ctx:SlashContext,platform:str,gemi:str):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		shipRole = get(ctx.guild.roles,name=str(gemi))
		embed = discord.Embed(title="Puan Artışı",description=f"**{shipRole.mention}** adlı geminin mürettebatına **{platformXPs[platform]}** puan eklendi!")
		await ctx.send(embed=embed)
		__addPointToSpaceShip(ctx.guild.members, platform, shipRole)



@slash.slash(
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
async def _kişiselpuan(ctx:SlashContext,kullanıcı:discord.Member,puan:int):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		user = User(kullanıcı.id)
		user.addXP(puan)
		
		embed=discord.Embed(title="Puan ekleme işlemi",description=f"**{kullanıcı.name}** adlı kullanıcıya **{puan}** puan eklendi!",color=kullanıcı.top_role.color)
		await ctx.send(embed=embed)
	else:
		await ctx.send("Bu komutu kullanmaya izniniz yok!")


@slash.slash(
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
async def createRole(ctx,rol,emoji):
	guild = ctx.guild
	roleName = f"{rol} {emoji}"
	await guild.create_role(name=roleName)
	role = get(guild.roles,name=roleName)
	await ctx.send(embed=discord.Embed(title="Rol oluşturma işlemi",description=f"{role.mention} rolü oluşturuldu."))





@slash.slash(
	name = "yetenekağacı",
	description = "Yetenek ağacına rol eklemek için kullan!",
	guild_ids = guildID,
	options=[
		create_option(
			name= "rol",
			description = "Bir rol seç.",
			option_type=8,
			required=True, 
		),
		create_option(
			name = "emoji",
			description="Bir emoji gir.",
			option_type=3,
			required=True,
		),
		create_option(
			name="message_id",
			description = "Emojinin eklenmesini istediğin mesaj id'sini gir.",
			option_type=3,
			required=True
		)
		
		]
)
async def embed(ctx,rol,emoji:str,message_id:int):
	channel = client.get_channel(905888377071616090)
	message = await channel.fetch_message(911627236510146611)
	embed = message.embeds[0]
	di = embed.to_dict()
	description = str(di['description'])
	description += "\n"+f"{emoji}:{str(rol)[:-2]}"
	di['description'] = description
	embed = discord.Embed.from_dict(di)
	dictionary[str(emoji)] = str(rol)
	with open("files/embedDictionary.py","w") as dosya:
		dosya.write("dictionary = ")
		dosya.close()
	with open("files/embedDictionary.py","a",encoding="utf-8") as dosya:
		dosya.write(str(dictionary))
		dosya.close()
	await message.edit(embed=embed)
	emojiMessage = await channel.fetch_message(message_id)
	await emojiMessage.add_reaction(str(emoji))
	await ctx.send(embed=discord.Embed(title="Yetenek ağacı güncellemesi",description=f"{str(rol.mention)} rolü yetenek ağacına eklendi!"))



async def createChannel(ctx,name,category):
	guild = ctx.guild
	await guild.create_text_channel(name=name,category=category)

async def createVC(ctx,name,category):
	guild = ctx.guild
	await guild.create_voice_channel(name=name,category=category)

@slash.slash(
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
async def _createSpaceShip(ctx:SlashContext,gemi):
	guild = ctx.guild
	await guild.create_role(name=f"🚀{gemi}")
	await guild.create_role(name=f"🚀{gemi} - Captain")
	unit = get(guild.roles,name="Unit")
	shipRole = get(guild.roles,name=f"🚀{gemi}")
	captain = get(guild.roles,name=f"🚀{gemi} - Captain")
	embed = discord.Embed(
		title = "Gemi Oluşturma İşlemi",
		description = f"{shipRole.mention} gemisi oluşturuluyor",
		color = 0x8d42f5
	)
	embedMessage = await ctx.channel.send(embed=embed)
	overwrites = {
		unit : discord.PermissionOverwrite(
			view_channel=True,
			read_messages=True,
			send_messages=False,
			speak=False,
			read_message_history=True,
			stream=False,
			connect=True,),
		shipRole : discord.PermissionOverwrite(
			view_channel=True,
			read_messages=True,
			send_messages=True,
			speak=True,
			read_message_history=True,
			stream=True,
			add_reactions=True,
			attach_files=True,
			connect=True,
			embed_links=True,
			use_external_emojis=True,),
		captain : discord.PermissionOverwrite(
			view_channel=True,
			read_messages=True,
			send_messages=True,
			speak=True,
			read_message_history=True,
			stream=True,
			manage_messages=True,
			manage_channels=True,
			add_reactions=True,
			attach_files=True,
			deafen_members=True,
			connect=True,
			use_external_emojis=True,
			embed_links=True,
			mute_members=True,
			move_members=True,)
	}
	category = await guild.create_category(name=f"🚀{gemi}",overwrites=overwrites)
	await createChannel(ctx,f"🚀{gemi}-hall",category)
	await createChannel(ctx,"📓captain-s-logbook",category)
	await createChannel(ctx,"💬chat-box",category)
	await createChannel(ctx,"🧠brai̇nstorm-notes",category)
	await createChannel(ctx,"📋checklist",category)
	await createChannel(ctx,"🔗reference-archive",category)
	await createChannel(ctx,"📜documents",category)
	await createChannel(ctx,"🎨visual-arts",category)
	await createChannel(ctx,"🎹sound-arts",category)

	await createVC(ctx,"🟥 Red Room",category)
	await createVC(ctx,"⬛ Black Room",category)
	await createVC(ctx,"🟩 Green Room",category)


	gemi = str(f"🚀{gemi}").lower()
	captainsHall = get(guild.channels,name=f"{gemi}-hall")

	message = await captainsHall.send("**Geminin kaptanını** belirlemek için, **kaptan** olacak kişinin aşağıdaki emojiye basması gerekmektedir.\n**Uyarı**, bu **tek seferlik** bir seçim olduğu için, tıklamadan önce **iyice karar vermeniz** tavsiye edilir.")

	await message.add_reaction("🚀")

	captainHalls[str(shipRole)] = (captainsHall.id)
	with open("files/openShips.py","w",encoding="utf-8") as dosya:
		dosya.write("captainHalls = ")
		dosya.write(str(captainHalls)+"\n")

		dosya.close()
	embed = discord.Embed(
		title = "Gemi Oluşturma İşlemi",
		description = f"{shipRole.mention} gemisi oluşturuldu. Katılacak mürettebatın dikkatine!",color=0x8d42f5
	)
	await embedMessage.edit(embed=embed)

@slash.slash(
	name="gemipatlat",
	description="Bir gemiyi imha etmek için kullan.",
	guild_ids=guildID,
	options=[
		create_option(
			name="gemi",
			description="İmha edilecek geminin ismini girin.",
			option_type=3,
			required=True
		),
		create_option(
			name="kategori",
			description="İmha edilecek geminin bulunduğu kategoriyi seçiniz.",
			option_type=7,
			required=True
		)
	]
)
async def _gemipatlat(ctx,gemi,kategori:int):
	guild = ctx.guild
	role = get(guild.roles,name=f"🚀{gemi}")
	captainRole = get(guild.roles,name=f"🚀{gemi} - Captain")
	embed = discord.Embed(
		title = "Gemi İmha İşlemi",
		description = f"{role.mention} gemisi patlatılıyor!",
		color = 0x8d42f5
	)
	message = await ctx.send(embed=embed)
	channel = client.get_channel(id = kategori.id)
	for channel in channel.text_channels:
		await channel.delete()
	channel = client.get_channel(id = kategori.id)
	for voicechannel in channel.voice_channels:
		await voicechannel.delete()
	await channel.delete()
	
	await role.delete()
	await captainRole.delete()
	del captainHalls[f'🚀{gemi}']
	with open("files/openShips.py","w",encoding="utf-8") as dosya:
		dosya.write("captainHalls = ")
		dosya.write(str(captainHalls))
		dosya.close()
	embed = discord.Embed(
		title = "İşlem Başarılı!",
		description = "Gemi başarıyla imha edildi!",
		color = 0x8d42f5
	)
	await message.edit(embed=embed)

""" 
	TEST COMMANDS
"""
@client.command()
async def embedDuzenle(ctx):
	channel = client.get_channel(905888377071616090)
	message = await channel.fetch_message(911627236510146611)
	embed = message.embeds[0]
	di = embed.to_dict()
	# await ctx.channel.send(di)
	# description = str(di['description'])
	description = "Gemide eksik olan mürettebat sen olabilirsin.\nYeteneklerini işaretle! Rolünü seç! Gizli yetenek olmaktan çık!\n"
	for emoji,rol in dictionary.items():
		description += "\n"+f"{emoji}:{str(rol)[:-2]}"
		di['description'] = description
	embed = discord.Embed.from_dict(di)
	dictionary[str(emoji)] = str(rol)
	await message.edit(embed=embed)

@client.command()
async def mesajsil(ctx):
	await ctx.message.delete()
	try:
		message = await ctx.channel.fetch_message(info[ctx.author.id])
		await message.delete()
		del info[ctx.author.id]
		with open("files/infoMessage.py","w",encoding="utf-8") as dosya:
			dosya.write("info = ")
			dosya.write(str(info))
		embed=discord.Embed(
			title = "Uyarı",
			description = "Bilgi mesajı silindi!",
			color = 0xFF0000
		)
		message = await ctx.channel.send(embed=embed)
		await asyncio.sleep(3)
		await message.delete()
	except KeyError:
		embed = discord.Embed(
			title = "Uyarı",
			description = "Olmayan bir mesajı silemezsin!",
			color = 0xFF0000
		)
		message = await ctx.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()
		
	except discord.errors.NotFound:
		embed = discord.Embed(
			title = "Uyarı",
			description = "Olmayan bir mesajı silemezsin!",
			color = 0xFF0000
		)
		message = await ctx.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()
	

@client.command()
async def bilgi(ctx):
	await ctx.message.delete()
	try:
		if info[ctx.author.id]:
			embed = discord.Embed(
				title = "Uyarı",
				description = "Eski mesajını silmeden yeni bir tane mesaj açamazsın!\nEski mesajının nerede olduğunu hatırlamıyorsan `!mesajsil` komutunu kullanabilirsin.",
				color = 0xFF0000
			)
			message = await ctx.channel.send(embed=embed)
			await asyncio.sleep(5)
			await message.delete()
	except KeyError:
		embed = discord.Embed(title="Üye Bilgi Ekranı",description="Üye bilgi ekranına hoş geldin.\nAşağıdaki butonlara basarak\nbilgisini almak istediğin içeriği görebilirsin.",color = 0x8d42f5,)
		embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		message = await ctx.channel.send(
			embed=embed,
			components = [
				Button(
					label = "Mevcut Seviye",
					custom_id = "seviye",
					color = ButtonStyle.Green,
					emoji = "📰",
				),
				Button(
					label = "Liderlik Tablosu",
					custom_id = "liderliktablosu",
					color = ButtonStyle.Green,
					emoji = "📋",
				),
				Button(
					label = "Detaylı Bilgi",
					custom_id = "detaylıbilgi",
					color = ButtonStyle.Green,
					emoji = "📜",
					new_line=True
				),
				Button(
					label="Görevler",
					custom_id = "görevler",
					color = ButtonStyle.Green,
					emoji = "🪧",
				),
				Button(
					label="Seviyeler",
					custom_id = "seviyeler",
					color = ButtonStyle.Green,
					emoji = "🚩",
					new_line=True
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
					
				),
				]
		)
		info[ctx.author.id] = message.id
		with open("files/infoMessage.py","w",encoding="utf-8") as dosya:
			dosya.write("info =")
			dosya.write(str(info))


@ui.components.listening_component('seviye')
async def listening_component(component):
	try:
		if component.message.id != info[component.author.id]:
			embed = discord.Embed(
				title = "Uyarı",
				description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
				color = 0xFF0000
			)
			try:
				await component.respond()
			except:
				pass
			message = await component.channel.send(embed=embed)
			await asyncio.sleep(5)
			await message.delete()
		else:
			await component.message.edit(components=[
				Button(
					label = "Mevcut Seviye",
					custom_id = "seviye",
					color = ButtonStyle.Green,
					emoji = "📰",
					disabled=True
				),
				Button(
					label = "Liderlik Tablosu",
					custom_id = "liderliktablosu",
					color = ButtonStyle.Green,
					emoji = "📋",
					disabled=True
				),
				Button(
					label = "Detaylı Bilgi",
					custom_id = "detaylıbilgi",
					color = ButtonStyle.Green,
					emoji = "📜",
					new_line=True,
					disabled=True
				),
				Button(
					label="Görevler",
					custom_id = "görevler",
					color = ButtonStyle.Green,
					emoji = "🪧",
					disabled=True
				),
				Button(
					label="Seviyeler",
					custom_id = "seviyeler",
					color = ButtonStyle.Green,
					emoji = "🚩",
					new_line=True,
					disabled=True
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
					disabled=True
					
				),
				])
			try:
				await component.respond()
			except:
				pass
			member = component.author
			user = User(member.id)
			if not member.bot:
				embed = discord.Embed(title=f"{member.name}#{member.discriminator} adlı kullanıcının değerleri",description="",color=0x8d42f5)
				embed.add_field(name="Mevcut değerler - 🏆 ",value="Seviyesi = **{}**\n Puanı = **{}**\n Rütbesi = **{}**\n".format(user.level,user.XP,user.levelName,inline=False))
				if user.haveMaxLevel():
					embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**Maksimum seviyeye ulaştınız!**",inline=False)
				elif not user.haveMaxLevel():
					if experiences[user.level-2] - user.XP <= 0:
						embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.getLevel(user.XP)-2]}** rütbesine ulaştın! Seviye atlamak için ses kanalına girebilirsin.",inline=False)
					else:
						embed.add_field(name="Bir sonraki rütbe - 🚀 ",value=f"**{levelNames[user.level]}** rütbesi için kalan puan = **{(experiences[user.level-2])-user.XP}**",inline=False)

				embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
			
			await component.message.edit(embed=embed,components=[
				Button(
					label="Geri",
					custom_id="geri",
					color=ButtonStyle.Grey,
					emoji="⬅️"
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
				)
				])

	except KeyError:
		embed = discord.Embed(
				title = "Uyarı",
				description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
				color = 0xFF0000
			)
		try:
			await component.respond()
		except:
			pass
		message = await component.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()
		return
		

	try:
		await component.respond()
	except:
		pass
		

	

@ui.components.listening_component('liderliktablosu')
async def listening_component(component):
	try:
		if component.message.id != info[component.author.id]:
			embed = discord.Embed(
				title = "Uyarı",
				description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
				color = 0xFF0000
			)
			try:
				await component.respond()
			except:
				pass
			message = await component.channel.send(embed=embed)
			await asyncio.sleep(5)
			await message.delete()
		else:
			await component.message.edit(components=[
				Button(
					label = "Mevcut Seviye",
					custom_id = "seviye",
					color = ButtonStyle.Green,
					emoji = "📰",
					disabled=True
				),
				Button(
					label = "Liderlik Tablosu",
					custom_id = "liderliktablosu",
					color = ButtonStyle.Green,
					emoji = "📋",
					disabled=True
				),
				Button(
					label = "Detaylı Bilgi",
					custom_id = "detaylıbilgi",
					color = ButtonStyle.Green,
					emoji = "📜",
					new_line=True,
					disabled=True
				),
				Button(
					label="Görevler",
					custom_id = "görevler",
					color = ButtonStyle.Green,
					emoji = "🪧",
					disabled=True
				),
				Button(
					label="Seviyeler",
					custom_id = "seviyeler",
					color = ButtonStyle.Green,
					emoji = "🚩",
					new_line=True,
					disabled=True
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
					disabled=True			
				),
			])
			try:
				await component.respond()
			except:
				pass
			sortedMembers = getSortedMembers(component)

			embed=discord.Embed(title="Sıralama",inline=False,color=0x8d42f5)
			embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)

			count = 1
			
			for key,value in sortedMembers.items():
				embed.add_field(name="{} - {}".format(count,key),value="**Puan**: {}\n**Rütbe**: {}".format(value[0],value[1]),inline=False)
				count += 1
				if count == 11:break

			await component.message.edit(embed=embed,components=[
				Button(
					label="Geri",
					custom_id="geri",
					color=ButtonStyle.Grey,
					emoji="⬅️"
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
				)
			])
	except KeyError:
		embed = discord.Embed(
			title = "Uyarı",
			description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
			color = 0xFF0000
		)
		try:
			await component.respond()
		except:
			pass
		message = await component.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()


@ui.components.listening_component('detaylıbilgi')
async def listening_component(component):
	try:
		if component.message.id != info[component.author.id]:
			embed = discord.Embed(
				title = "Uyarı",
				description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
				color = 0xFF0000
			)
			try:
				await component.respond()
			except:
				pass
			message = await component.channel.send(embed=embed)
			await asyncio.sleep(5)
			await message.delete()
		else:		
			await component.message.edit(components=[
				Button(
					label = "Mevcut Seviye",
					custom_id = "seviye",
					color = ButtonStyle.Green,
					emoji = "📰",
					disabled=True
				),
				Button(
					label = "Liderlik Tablosu",
					custom_id = "liderliktablosu",
					color = ButtonStyle.Green,
					emoji = "📋",
					disabled=True
				),
				Button(
					label = "Detaylı Bilgi",
					custom_id = "detaylıbilgi",
					color = ButtonStyle.Green,
					emoji = "📜",
					new_line=True,
					disabled=True
				),
				Button(
					label="Görevler",
					custom_id = "görevler",
					color = ButtonStyle.Green,
					emoji = "🪧",
					disabled=True
				),
				Button(
					label="Seviyeler",
					custom_id = "seviyeler",
					color = ButtonStyle.Green,
					emoji = "🚩",
					new_line=True,
					disabled=True
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
					disabled=True			
				),
			])
			liste = {}
			XP = {}
			for i in range(1,11):
				liste[f'level{i}'] = 0
				XP[f'xp{i}'] = ""
				if i == 1:
					XP[f"xp{i}"] += f"{levelNames[i-1]}"
				else:
					XP[f'xp{i}'] += f"{levelNames[i-1]} - {experiences[i-2]}" 

			try:
				await component.respond()
			except:
				pass
			
			for member in client.get_all_members():
				if not member.bot:
					user = User(member.id)
					liste[f'level{user.level}'] += 1
			
			message = discord.Embed(title = "Detaylı Bilgi",description="**Aşağıda, hangi seviyede kaç kullanıcının bulunduğunu öğrenebilirsin**",color = 0x8d42f5)
			
			for level in range(1,11):
				XPs = XP[f'xp{level}']
				levels = liste[f'level{level}']		
				if levels == 0:
					if XP[f'xp{level}'] == "Guest":
						message.add_field(name=f"*Seviye {level}* / {XPs}:",value=f"Bu seviyede herhangi biri yok.",inline=False)
					else:
						message.add_field(name=f"*Seviye {level}* / {XPs} XP:",value=f"Bu seviyede herhangi biri yok.",inline=False)
					
					
				else:
					if XP[f'xp{level}'] == "Guest":
						message.add_field(name=f"*Seviye {level}* / {XPs}:",value=f"**{levels}** kişi bu seviyede.",inline=False)
					else:
						message.add_field(name=f"*Seviye {level}* / {XPs} XP:",value=f"**{levels}** kişi bu seviyede.",inline=False)
			message.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
			await component.message.edit(embed=message,components=[
				Button(
					label="Geri",
					custom_id="geri",
					color=ButtonStyle.Grey,
					emoji="⬅️"
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
				)

				])
	
	except KeyError:
		embed = discord.Embed(
			title = "Uyarı",
			description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
			color = 0xFF0000
		)
		try:
			await component.respond()
		except:
			pass
		message = await component.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()		
			
				
	
	
@ui.components.listening_component('görevler')
async def listening_component(component):
	try:
		if component.message.id != info[component.author.id]:
			embed = discord.Embed(
				title = "Uyarı",
				description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
				color = 0xFF0000
			)
			try:
				await component.respond()
			except:
				pass
			message = await component.channel.send(embed=embed)
			await asyncio.sleep(5)
			await message.delete()
		else:
			await component.message.edit(components=[
				Button(
					label = "Mevcut Seviye",
					custom_id = "seviye",
					color = ButtonStyle.Green,
					emoji = "📰",
					disabled=True
				),
				Button(
					label = "Liderlik Tablosu",
					custom_id = "liderliktablosu",
					color = ButtonStyle.Green,
					emoji = "📋",
					disabled=True
				),
				Button(
					label = "Detaylı Bilgi",
					custom_id = "detaylıbilgi",
					color = ButtonStyle.Green,
					emoji = "📜",
					new_line=True,
					disabled=True
				),
				Button(
					label="Görevler",
					custom_id = "görevler",
					color = ButtonStyle.Green,
					emoji = "🪧",
					disabled=True
				),
				Button(
					label="Seviyeler",
					custom_id = "seviyeler",
					color = ButtonStyle.Green,
					emoji = "🚩",
					new_line=True,
					disabled=True
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
					disabled=True			
				),
				])
			try:
				await component.respond()
			except:
				pass
			embed = discord.Embed(
				title = "Görevler",
				description = "**Bir gemiye atla ve bir oyun üret**;\nPC/Platform .............................. 10.0000 XP\nMobil ............................................... 5.000 XP\nHyperCasual................................... 2.000 XP\nGameJam.......................................... 1.000XP\n*Oyun yayınlanırsa kazanılan deneyim puanı iki katına çıkar*",
				color = 0x8d42f5
			)
			embed.add_field(
				name = "\n\nSunucu Takviyesi",
				value = "Her sunucu takviyesi başına **250 XP**",
				inline=False
			)
			embed.add_field(
				name = "\n\nSes Kanallarına Aktif Ol",
				value = "Dakika başına 1 XP\n*Not: Kazanılan XP, yayın ve kamera açma durumuna göre değişiklik gösterir.*",
				inline=False
			)
			embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
			await component.message.edit(embed=embed,components=[
				Button(
					label="Geri",
					custom_id="geri",
					color=ButtonStyle.Grey,
					emoji="⬅️"
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
				)
				])
	
	except KeyError:
		embed = discord.Embed(
			title = "Uyarı",
			description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
			color = 0xFF0000
		)
		try:
			await component.respond()
		except:
			pass
		message = await component.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()


@ui.components.listening_component('seviyeler')
async def listening_component(component):
	try:
		if component.message.id != info[component.author.id]:
			embed = discord.Embed(
				title = "Uyarı",
				description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
				color = 0xFF0000
			)
			try:
				await component.respond()
			except:
				pass
			message = await component.channel.send(embed=embed)
			await asyncio.sleep(5)
			await message.delete()
		else:

			await component.message.edit(components=[
				Button(
					label = "Mevcut Seviye",
					custom_id = "seviye",
					color = ButtonStyle.Green,
					emoji = "📰",
					disabled=True
				),
				Button(
					label = "Liderlik Tablosu",
					custom_id = "liderliktablosu",
					color = ButtonStyle.Green,
					emoji = "📋",
					disabled=True
				),
				Button(
					label = "Detaylı Bilgi",
					custom_id = "detaylıbilgi",
					color = ButtonStyle.Green,
					emoji = "📜",
					new_line=True,
					disabled=True
				),
				Button(
					label="Görevler",
					custom_id = "görevler",
					color = ButtonStyle.Green,
					emoji = "🪧",
					disabled=True
				),
				Button(
					label="Seviyeler",
					custom_id = "seviyeler",
					color = ButtonStyle.Green,
					emoji = "🚩",
					new_line=True,
					disabled=True
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
					disabled=True			
				),
				])
			try:
				await component.respond()
			except:
				pass
			embed = discord.Embed(
				title = "Seviyeler",
				description = "Aşağıda, sunucuda bulunan mevcut seviyeleri görebilirsin.",
				color = 0x8d42f5
			)
			embed.add_field(
				name = "Guest:",
				value = "Misafir statüsünde üye",
				inline = False,

			)
			embed.add_field(
				name = "Colony Member / 250 XP:",
				value = "Koloni üyesi",
				inline = False,
			)

			embed.add_field(
				name = "Open Crew / 1.987 XP:",
				value = "Açık gemilerde mürettebat olma hakkına sahip üye",
				inline = False,
			)
			embed.add_field(
				name = "Crew / 6.666 XP:",
				value = "Bütün gemilerde mürettebat olma hakkına sahip üye",
				inline = False,
			)
			embed.add_field(
				name = "Captain / 9.999 XP:",
				value = "Gemilere kaptanlık yapma hakkına sahip üye",
				inline = False,
			)
			embed.add_field(
				name = "Judge / 30.000 XP:",
				value = "Oy kullanma hakkına sahip üye",
				inline = False,
			)
			embed.add_field(
				name = "Colony Manager / 90.000 XP:",
				value = "Tasarlanacak oyunlara karar veren üye",
				inline = False,
			)
			embed.add_field(
				name = "Mars Lover / 300.000 XP:",
				value = "Yayınlanan bütün oyunlarda adına teşekkür edilen üye",
				inline = False,
			)
			embed.add_field(
				name = "Chief of the Colony / 900.000 XP:",
				value = "Kolonideki kamu yönetiminde, herhangi bir rolü alabilen üye, A.K.A Chief",
				inline = False,
			)
			embed.add_field(
				name = "Partner / 10.000.001 XP:",
				value = "Koloninin fahri ortağı",
				inline = False,
			)
			embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
			await component.message.edit(embed=embed,components = [
				Button(
					label="Geri",
					custom_id="geri",
					color=ButtonStyle.Grey,
					emoji="⬅️"
				),
				Button(
					label = "Mesajı Sil",
					custom_id = "sil",
					color = ButtonStyle.Red,
				)
				])
	except KeyError:
		embed = discord.Embed(
			title = "Uyarı",
			description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
			color = 0xFF0000
		)
		try:
			await component.respond()
		except:
			pass
		message = await component.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()

@ui.components.listening_component('geri')
async def listening_component(component):
	try:
		if component.message.id != info[component.author.id]:
				embed = discord.Embed(
					title = "Uyarı",
					description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
					color = 0xFF0000
				)
				try:
					await component.respond()
				except:
					pass
				message = await component.channel.send(embed=embed)
				await asyncio.sleep(5)
				await message.delete()
		else:
			embed = discord.Embed(title="Üye Bilgi Ekranı",description="Üye bilgi ekranına hoş geldin.\nAşağıdaki butonlara basarak\nbilgisini almak istediğin içeriği görebilirsin.",color = 0x8d42f5)
			embed.set_author(name=component.author.display_name, icon_url=component.author.avatar_url)
			try:
				await component.respond()
			except:
				pass
			await component.message.edit(
				embed=embed,
				components = [
					Button(
						label = "Mevcut Seviye",
						custom_id = "seviye",
						color = ButtonStyle.Green,
						emoji = "📰",

					),
					Button(
						label = "Liderlik Tablosu",
						custom_id = "liderliktablosu",
						color = ButtonStyle.Green,
						emoji = "📋",

					),
					Button(
						label = "Detaylı Bilgi",
						custom_id = "detaylıbilgi",
						color = ButtonStyle.Green,
						emoji = "📜",
						new_line=True,

					),
					Button(
						label="Görevler",
						custom_id = "görevler",
						color = ButtonStyle.Green,
						emoji = "🪧",
			
					),
					Button(
						label="Seviyeler",
						custom_id = "seviyeler",
						color = ButtonStyle.Green,
						emoji = "🚩",
						new_line=True,

					),
					Button(
						label = "Mesajı Sil",
						custom_id = "sil",
						color = ButtonStyle.Red,
				
					),
					]
			)
	
	except KeyError:
		embed = discord.Embed(
			title = "Uyarı",
			description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
			color = 0xFF0000
		)
		try:
			await component.respond()
		except:
			pass
		message = await component.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()

@ui.components.listening_component('sil')
async def listening_component(component):
	try:
		if component.message.id != info[component.author.id]:
			embed = discord.Embed(
				title = "Uyarı",
				description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
				color = 0xFF0000
			)
			try:
				await component.respond()
			except:
				pass
			message = await component.channel.send(embed=embed)
			await asyncio.sleep(5)
			await message.delete()
			await component.message.delete()
		else:
			try:
				await component.respond()
			except:
				pass
			await component.message.delete()
			del info[component.author.id]
			with open("files/infoMessage.py","w",encoding="utf-8") as dosya:
				dosya.write("info = ")
				dosya.write(str(info))
	
	except KeyError:
		embed = discord.Embed(
			title = "Uyarı",
			description = "Bu senin mesajın değil!\nKendini mesajını oluşturmak için `!bilgi`",
			color = 0xFF0000
		)
		try:
			await component.respond()
		except:
			pass
		message = await component.channel.send(embed=embed)
		await asyncio.sleep(5)
		await message.delete()


@client.command()
async def mesaj(ctx,id_:int):
	if ctx.author.id == 373457193271558145 or ctx.author.id == 275971871047024640:
		guild = ctx.guild
		member = guild.get_member(user_id=id_)
		channel = client.get_channel(id=910547555245494322)
		await channel.send(f"{member.mention}, <#901248994922098718> kanalında kendinizi tanıttığınız için 250 XP kazandınız!")

client.run(TOKEN)


