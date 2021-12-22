class error():
    you_not_in_vc = "**💛🎻 {}, please connect to a vc first.**"
    not_connected_to_vc = "**🧡🎻 {}, I'm not connected to any vc.**"
    need_song_name = "**🧡🎻 {}, please may I have the name of the song you want to play.**"
    song_not_found = "**❤️🎻 {}, sorry I could not find that song anywhere.**"
    nothing_playing = "**🧡🎻 {}, I'm not playing anything.**"

class footer():
    type_1 = "🎻Goldy Music - V{}"

class playing():
    class embed():
        title = "**▶️ Now Playing**"
        des = """
        **``{}``**
        
        **• Requested by {} ┃ Duration: ``{}``**
        """

        footer = "Streaming from {}  •  {}"

    class crossed_out_embed():
        title = "~~**▶️ Now Playing**~~"
        des = """
        ~~**``{}``**~~
        
        ~~**• Requested by {} ┃ Duration: ``{}``**~~
        """

        footer = "Streaming from {}  •  {}"

class add_to_queue():
    class embed():
        title = "**➕ Added to Queue**"

        des = """
        **``{}`` added to queue.**

        **• Added by {} ┃ Duration: ``{}``**
        """

        footer = "Will stream from {}  •  {}"

class paused():
    class embed():
        title = "**⏸️ Paused**"

        des = """
        **{}, song paused.**
        """