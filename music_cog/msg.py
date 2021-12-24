class error():
    you_not_in_vc = "**💛🎻 {}, please connect to a vc first.**"
    not_connected_to_vc = "**🧡🎻 {}, your not connected to any vc.**"
    another_vc = "**💛🎻 {}, I'm already playing in another vc, join {} to control.**"
    need_song_name = "**🧡🎻 {}, please may I have the name of the song you want to play.**"
    song_not_found = "**❤️🎻 {}, sorry I could not find that song anywhere.**"
    nothing_playing = "**🧡🎻 {}, nothing is playing right now.**"

class footer():
    type_1 = "🎻Goldy Music - V{}"

class playing():
    class embed():
        title = "**▶️ Now Playing**"
        des = """
        **``{}``**
        
        **• Requested by {} ┃ Duration: ``{}`` ┃ Quality: ``{}``**
        """

        footer = "Streaming from {}  •  {}"

    class crossed_out_embed():
        title = "~~**▶️ Now Playing**~~"
        des = """
        ~~**``{}``**~~
        
        ~~**• Requested by {} ┃ Duration: ``{}`` ┃ Quality: ``{}``**~~
        """

        footer = "Streaming from {}  •  {}"

class add_to_queue():
    class embed():
        title = "**➕ Added to Queue**"

        des = """
        **``{}`` added to queue.**

        **• Added by {} ┃ Duration: ``{}`` ┃ Quality: ``{}``**
        """

        footer = "Will stream from {}  •  {}"

class add_to_queue_playlist():
    class embed():
        title = "**➕📜 Playlist Added to Queue**"

        des = """
        **``{}`` songs added to queue.**

        **• Added by {}**
        """

        footer = "Will stream from {}  •  {}"

class paused():
    class embed():
        title = "**⏸️ Paused**"

        des = """
        **{}, song paused.**
        """

class skipped():
    class embed():
        title = "**⏭️ Skipped**"

        des = """
        **``{}`` skipped.**
        """

class queue():
    class embed():
        title = "**➕ Songs in Queue ➕**"

class queue_remove():
    class embed():
        title = "**❌ Removed from Queue**"

        des = """
        **``{}`` removed from the queue.**
        """

class queue_song_is_playing():
    class embed():
        title = "**❌🎻 Cannot remove Song**"

        des = """
        **{}, this song can not be removed from the queue, as it's currently being played. Use the ``!skip`` command instead.**
        """

class clear():
    class embed():
        title = "**🤍🎻 Cleared Queue**"

        des = """
        **{}, all songs removed from queue.**
        """