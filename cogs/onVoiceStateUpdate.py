from discord.ext import commands
from functions.userClass import User

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

class OnVoiceStateUpdate(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,prev,cur):
        if not member.bot:
            user = User(member.id)
            
            if memberSituation(prev,cur) == "stream":
                modifier = user.getModifier(modifierType="Yayın Çarpanı")
                user.update("modifier",modifier)
                
            elif memberSituation(prev,cur) == "cam":
                modifier = user.getModifier(modifierType="Kamera Çarpanı")
                user.update("modifier",modifier)
                
            elif memberSituation(prev,cur) == "stream + cam":
                camModifier = user.getModifier(modifierType="Kamera Çarpanı")
                streamModifier = user.getModifier(modifierType="Yayın Çarpanı")
                modifier = camModifier + streamModifier
                user.update("modifier",modifier)
                
            elif memberSituation(prev,cur) == "":
                modifier = user.getModifier(modifierType="Dakika Çarpanı")
                user.update("modifier",modifier)


def setup(client):
    client.add_cog(OnVoiceStateUpdate(client))