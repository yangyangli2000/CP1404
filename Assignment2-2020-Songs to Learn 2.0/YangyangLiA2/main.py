"""
Songs To Learn 2.0 - CP1404 - Assessment 2
Name: YangYang Li
Date started: 29/05/2020
GitHub URL: (private) https://github.com/cp1404-students/a2-songs-to-learn-yangyangli714
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from songlist import SongList


class SongsList(App):
    def __init__(self, **kwargs):
        """
            This function will installing all the required widgets for the layout of kivy app
        """
        super().__init__(**kwargs)
        self.song_list = SongList()

        #   Bottom status label and Top count label
        self.top_label = Label(text="", id="count_label")
        self.status_label = Label(text="")

        # layout widget left part
        self.sort_label = Label(text="Sort by:")

        # Sets default sort method as Artist
        self.spinner = Spinner(text='Artist', values=('Artist', 'Title', 'Year', 'Required'))
        self.add_song_label = Label(text="Add New Song...")
        self.title_label = Label(text="Title:")
        self.title_text_input = TextInput(write_tab=False, multiline=False)
        self.artist_label = Label(text="Artist:")
        self.artist_text_input = TextInput(write_tab=False, multiline=False)
        self.year_label = Label(text="Year:")
        self.year_text_input = TextInput(write_tab=False, multiline=False)

        # To add and clear for the bottom widget
        self.add_song_button = Button(text='Add Song')
        self.clear_button = Button(text='Clear')

    def songs_sort(self, *args):
        """
        This function will sorts the songs base on the click of the spinner
        """
        self.song_list.sort(self.spinner.text)
        self.root.ids.rightLayout.clear_widgets()
        self.right_widgets()

    def build(self):
        """
            This function will opening the kivy app
        """
        self.title = "Songs List 2.0"
        self.root = Builder.load_file('app.kv')
        self.song_list.load_songs()
        self.song_list.sort('Artist')
        self.building_widgets()
        self.right_widgets()
        return self.root

    def building_widgets(self):
        """
            This function will left layout creation base on widgets created
        """
        self.root.ids.leftLayout.add_widget(self.sort_label)
        self.root.ids.leftLayout.add_widget(self.spinner)
        self.root.ids.leftLayout.add_widget(self.add_song_label)
        self.root.ids.leftLayout.add_widget(self.title_label)
        self.root.ids.leftLayout.add_widget(self.title_text_input)
        self.root.ids.leftLayout.add_widget(self.artist_label)
        self.root.ids.leftLayout.add_widget(self.artist_text_input)
        self.root.ids.leftLayout.add_widget(self.year_label)
        self.root.ids.leftLayout.add_widget(self.year_text_input)
        self.root.ids.leftLayout.add_widget(self.add_song_button)
        self.root.ids.leftLayout.add_widget(self.clear_button)
        self.root.ids.topLayout.add_widget(self.top_label)

        # Setting on click for sorting spinner, add button and clear button
        self.spinner.bind(text=self.songs_sort)
        self.add_song_button.bind(on_release=self.add_song_handler)
        self.clear_button.bind(on_release=self.clear_fields)

    def right_widgets(self):
        """
            This function will building right layout with widgets based on the list created.
        """
        # Sets the count label
        self.top_label.text = "To Learn: " + str(self.song_list.get_required_songs_count()) + ". Learned: " + str(
            self.song_list.get_learned_songs_count())

        # Check the status of the song and setts color based on it
        for song in self.song_list.songs:
            # l = Learned
            if song[0].status == 'l':
                song_button = Button(text='"' + song[0].title + '"' + " by " + song[0].artist + " (" + str(
                    song[0].year) + ") " "(Learned)", id=song[0].title)

                song_button.background_color = [88, 89, 0, 0.3]
            # u = Required to learn
            else:
                song_button = Button(
                    text='"' + song[0].title + '"' + " by " + song[0].artist + " (" + str(song[0].year) + ")",
                    id=song[0].title)

                song_button.background_color = [0, 88, 88, 0.3]

            # Setting on click for the buttons created
            song_button.bind(on_release=self.click_handler)
            self.root.ids.rightLayout.add_widget(song_button)

    def click_handler(self, button):
        """
            This function will change the status and show the updates to  the user
        """

        # if song is learned after user clicked button it change to required to learn
        if self.song_list.get_song(button.id).status == 'l':
            self.song_list.get_song(button.id).status = 'u'
            self.root.ids.bottomLayout.text = "You need to learn " + str(self.song_list.get_song(button.id).title)

        # if song is Required to learn after user clicked button it change to learned
        else:
            self.song_list.get_song(button.id).status = 'l'
            self.root.ids.bottomLayout.text = "You have learned " + str(self.song_list.get_song(button.id).title)

        # Update the sorting
        self.songs_sort()
        self.root.ids.rightLayout.clear_widgets()
        self.right_widgets()

    def clear_fields(self, *args):
        """
            This function will clearing up all the user input
        """
        self.title_text_input.text = ""
        self.artist_text_input.text = ""
        self.year_text_input.text = ""
        self.root.ids.bottomLayout.text = ""

    def add_song_handler(self, *args):
        """
            This function will do error checking for user input
        """
        # Checks if all the input fields are been filled in if not error text will be displayed
        if str(self.title_text_input.text).strip() == '' or str(self.artist_text_input.text).strip() == '' or str(
                self.year_text_input.text).strip() == '':
            self.root.ids.bottomLayout.text = "All fields must be completed"
        else:
            try:
                # Checks if year is negative if is error text will be displayed
                if int(self.year_text_input.text) < 0:
                    self.root.ids.bottomLayout.text = "Please enter a valid number"
                # Checks the format are correct
                else:
                    self.song_list.add_song(self.title_text_input.text, self.artist_text_input.text,
                                            int(self.year_text_input.text))
                    self.song_list.sort(self.spinner.text)
                    self.clear_fields()
                    self.root.ids.rightLayout.clear_widgets()
                    self.right_widgets()
            # Checks if year input is string if it is error text will be displayed
            except ValueError:
                self.root.ids.bottomLayout.text = "Please enter a valid number"

    def close(self):
        """
        This function will saved to to songs.csv file when the user try to close it
        """
        self.song_list.save_file()


if __name__ == '__main__':
    app = SongsList()
    app.run()
