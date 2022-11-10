
class Song:
    def __init__(self, title, artist, year, status):
        """
            This function will putting some attribute for the song
        """
        self.title = title
        self.artist = artist
        self.year = year
        self.status = status

    def mark_song(self, status):
        """
            This function will marking song as learnt ot not
        """
        self.status = status
