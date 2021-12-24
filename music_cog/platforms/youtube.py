import youtube_dl
import pafy
import asyncio

from src import goldy_error, goldy_func

from .. import config
from ... import music as ext #Music Cog

platform = "YouTube"
icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/2560px-YouTube_full-color_icon_%282017%29.svg.png" #This icon will be shown in the goldy music embeds.
common_url_domains = ["youtube.com/watch?", "youtu.be"]

async def search(ctx, client, song:str): #Searches for song on youtube and returns url.
    #Check if song is a url, if not assume it's just the name of a song.
    count = 0
    for common_url in common_url_domains:
        if common_url in song:
            count =+ 1

    if count == 0:
        #It's not a URL so perform a youtube search for the url.
        async with ctx.typing():
            try:
                info = youtube_dl.YoutubeDL({"format":"bestaudio", "quiet":False}).extract_info(f"ytsearch1:{song}", 
                download=False, ie_key="YoutubeSearch")

                if len(info["entries"]) == 0:
                    return None

                return info["entries"][0]["webpage_url"]

            except Exception as e:
                await goldy_error.log(ctx, client, e, None)
    else:
        #It is a url so just return it back.
        return song

class stream():
    def __init__(self, ctx, client, song_url):
        self.ctx = ctx
        self.client = client
        self.song_url = song_url
        self.loop = asyncio.get_event_loop()

        self.stream_object = self.loop.create_task(self.create()) #Create stream object for song.
        goldy_func.print_and_log("info_2", f"[{ext.cog_name.upper()}: {platform}] Stream created for '{song_url}'.")

    async def create(self): #Get's YouTube audio stream object.
        try:
            if not self.song_url == None:
                video = pafy.new(self.song_url)
                stream_object = video.getbestaudio()
                setattr(stream_object, "platform", __class__)
                setattr(stream_object.platform, "name", platform)
                setattr(stream_object.platform, "icon", icon)

                setattr(stream_object, "duration", __class__)
                setattr(stream_object.duration, "formated", video.duration)
                setattr(stream_object.duration, "unformated", video.duration)
                
                setattr(stream_object, "thumbnail", video.bigthumb)

                return stream_object
            else:
                goldy_func.print_and_log("warn", f"[{platform}] Url is none.")
                return False

        except Exception as e:
            await goldy_error.log(self.ctx, self.client, e, None)
            return False

    async def get(self): #Returns stream object.
        return self.stream_object

