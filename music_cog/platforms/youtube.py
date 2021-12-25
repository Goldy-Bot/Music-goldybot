import youtube_dl
import pafy
import asyncio
import pytube

from src import goldy_error, goldy_func

from .. import config
from ... import music as ext #Music Cog

platform = "YouTube"
icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/2560px-YouTube_full-color_icon_%282017%29.svg.png" #This icon will be shown in the goldy music embeds.
video_urls = ["youtube.com/watch?", "youtu.be"]
playlist_urls = ["youtube.com/playlist?list="]
common_url_domains = video_urls + playlist_urls

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

    async def create(self): #Get's YouTube audio stream object.
        try:
            if not self.song_url == None:
                for video_url in video_urls:
                    if video_url in self.song_url:
                        #It's a single song.
                        video = pafy.new(self.song_url)
                        stream_object = video.getbestaudio()
                        setattr(stream_object, "platform", __class__)
                        setattr(stream_object.platform, "name", platform)
                        setattr(stream_object.platform, "icon", icon)

                        setattr(stream_object, "duration", __class__)
                        setattr(stream_object.duration, "formated", video.duration)
                        setattr(stream_object.duration, "unformated", video.duration)
                        
                        setattr(stream_object, "thumbnail", video.bigthumb)
                        setattr(stream_object, "playlist", (False, None))

                        goldy_func.print_and_log("info_2", f"[{ext.cog_name.upper()}: {platform}] Stream created for '{self.song_url}'.")
                        return stream_object

                for playlist_url in playlist_urls:
                    if playlist_url in self.song_url:
                        #It's a playlist.
                        count = 0
                        stream_object_list = []
                        url_list = []
                        playlist = pytube.Playlist(self.song_url)
                        
                        async with self.ctx.typing():
                            for song in playlist: #Remove limit in production.
                                count += 1
                                video = pafy.new(song)
                                stream_object = video.getbestaudio()
                                setattr(stream_object, "platform", __class__)
                                setattr(stream_object.platform, "name", platform)
                                setattr(stream_object.platform, "icon", icon)

                                setattr(stream_object, "duration", __class__)
                                setattr(stream_object.duration, "formated", video.duration)
                                setattr(stream_object.duration, "unformated", video.duration)
                                
                                setattr(stream_object, "thumbnail", video.bigthumb)
                                setattr(stream_object, "playlist", (False, None))
                                
                                stream_object_list.append(stream_object)
                                url_list.append(song)

                        goldy_func.print_and_log("info_2", f"[{ext.cog_name.upper()}: {platform}] Streams created for all songs in the playlist '{self.song_url}'.")
                        return url_list, stream_object_list
            else:
                goldy_func.print_and_log("warn", f"[{platform}] Url is '{self.song_url}'.")
                return False

        except Exception as e:
            await goldy_error.log(self.ctx, self.client, e, None)
            return False

    async def get(self): #Returns stream object.
        return self.stream_object

