import requests
import os
import json
from datetime import datetime
from discord.ext import commands,tasks
from main import client

INSTAGRAM_USERNAME = os.environ['INSTAGRAM_USERNAME']

def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


def webhook(webhook_url, html):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 0x8d42f5
    embed["title"] = "Mars Game Colony / Instagram"
    embed["url"] = "https://www.instagram.com/p/" + \
		get_last_publication_url(html)+"/"
    embed["description"] = get_description_photo(html)
    embed["thumbnail"] = {"url": get_last_thumb_url(html)}
    embed['fields'] = [{'name':'\u200b','value':'\u200b'},{'name':'Sosyal Medya','value':'<:instagram:923593721499508766>   [Instagram](https://www.instagram.com/marsgamecolony/)\n<:twitter:923593743922257940>   [Twitter](https://twitter.com/marsgamecolony)\n<:linkedin:923593774326767636>    [LinkedIn](https://www.linkedin.com/company/mars-game-colony/about/?viewAsMember=true)\n<:youtube:923593791007510610>   [YouTube](https://www.youtube.com/channel/UCjonZWIIYc7ibxTliXHD3DQ)'}]
    embed['timestamp'] = str(datetime.utcnow())
    embed['footer'] = {'text':'@marsgamecolony',"icon_url":"https://i.hizliresim.com/k2dzgfw.jpg"}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))


def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html


def a():
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        with open("instagram.py") as dosya:
            okuma = dosya.read().splitlines()
            dosya.close()
        if okuma[0] == get_last_publication_url(html):
            pass
        else:
            with open("instagram.py","w") as dosya:
                dosya.write(get_last_publication_url(html))
                dosya.close()
            pass
            webhook(os.environ.get("WEBHOOK_URL"),
                    get_instagram_html(INSTAGRAM_USERNAME))
    except Exception as e:
        print(e)

class Instagram(commands.Cog):
    def __init__(self,client):
        self.client = client

        

    @tasks.loop(seconds=3)
    async def xyz():
        if os.environ.get('INSTAGRAM_USERNAME') != None and os.environ.get('WEBHOOK_URL') != None:
                a()
        else:
            print('Please configure environment variables properly!')
        
    @xyz.before_loop
    async def before_xyz():
        await client.wait_until_ready()
        print("Instagram Update Loop OK!")
    xyz.start()			


def setup(client):
    client.add_cog(Instagram(client))