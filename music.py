import os, sys
from tkinter import Tk, Frame, Scale, Label, Button, Listbox, Scrollbar
from tkinter import filedialog, messagebox
from pygame import mixer

class MusicPlayer:

    def __init__(self, root):
        self.root = root
        self.root.title("YourMood")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Set the icon
        icon_path = "music.ico"
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        # Initialize Pygame mixer
        mixer.init()  

        # Variables
        self.playlist = []
        self.volume = 0
        self.current_song_index = -1
        
        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Playlist frame
        self.playlist_frame = Frame(self.root)
        self.playlist_frame.pack(pady=20)

        self.playlist_label = Label(self.playlist_frame, text="Playlist")
        self.playlist_label.pack(pady=10)

        self.playlist_box = Listbox(self.playlist_frame, width=60)
        self.playlist_box.pack(side="right", fill="y")

        # self.current_song_frame = Frame(self.root)
        # self.current_song_frame.pack(pady=10)


        self.scrollbar = Scrollbar(self.playlist_frame, orient="vertical")
        self.scrollbar.config(command=self.playlist_box.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.playlist_box.config(yscrollcommand=self.scrollbar.set)

        
        # Checks for the command line input
        if len(sys.argv) > 1:
            self.play_song()
            self.add_songs_from_command_line()

        # 
        # self.current_song_label = Label(self.current_song_frame, text="", width=50)
        # self.current_song_label.pack()

        # self.current_song_scale = Scale(
        # self.current_song_frame, from_=0, to=mixer.Sound.get_length, orient="horizontal",
        # showvalue=True, command=mixer.music.set_pos
        # )
        # self.current_song_scale.pack(fill="x")
        
        # Buttons frame
        self.buttons_frame = Frame(self.root)
        self.buttons_frame.pack(pady=20)

        self.add_button = Button(self.buttons_frame, text="➕", command=self.add_song)
        self.add_button.grid(row=0, column=0)

        self.remove_button = Button(self.buttons_frame, text="➖", command=self.remove_song)
        self.remove_button.grid(row=0, column=1)

        self.previous_button = Button(self.buttons_frame, text="⏮️", command=self.previous_song)
        self.previous_button.grid(row=0, column=2, padx=(10,0))

        self.play_button = Button(self.buttons_frame, text="▶️", command=self.play_song)
        self.play_button.grid(row=0, column=3)

        self.next_button = Button(self.buttons_frame, text="⏭️", command=self.next_song)
        self.next_button.grid(row=0, column=5)

        self.pause_button = Button(self.buttons_frame, text="⏸️", command=self.pause_song)
        self.pause_button.grid(row=0, column=4)
        
        self.stop_button = Button(self.buttons_frame, text="⏹", command=self.stop_song)
        self.stop_button.grid(row=0, column=6)

        self.volume_scale = Scale(
            self.root, from_=0, to=100, orient="horizontal",
            label="🔊", command=self.set_volume,
        )
        self.volume_scale.pack(pady=(0,0))

    def add_songs_from_command_line(self):
        song_paths = sys.argv[1:]
        for song_path in song_paths:
            self.add_song_to_playlist(song_path.replace("\\","/")) # filedialog and add song have differet path formate.

    def add_song_to_playlist(self, song_path):
        song_name = os.path.basename(song_path)
        if song_name not in self.playlist:
            self.playlist_box.insert("end", "  " + song_name)
            self.playlist.append(song_path)
        else:
            messagebox.showinfo("Error", "Song already exists in the playlist!")

    # Add multiple song in the playlist
    def add_song(self):
        song_paths = filedialog.askopenfilenames(initialdir="C:\Users\Public\Music", title="Select Song", filetypes=(("Audio files", "*.mp3"),))
        for song_path in song_paths:
            if song_path not in self.playlist:
                self.add_song_to_playlist(song_path)
            else:
                messagebox.showinfo("Error", "Song already exists in the playlist!")            
    

    # Remove the songs in the playlist
    def remove_song(self):
        if len(self.playlist) == 0:
            messagebox.showinfo("Error", "Empty playlist!")
        else:
            selected_song = self.playlist_box.curselection()
            if selected_song:
                self.playlist_box.delete(selected_song)
                self.playlist.pop(selected_song[0])
                if selected_song[0] == self.current_song_index:
                    mixer.music.stop()
            else:
                messagebox.showinfo("Error", "No song selected!")

    # Load the song
    def load_song(self, song_index):
        song_path = self.playlist[song_index]
        mixer.music.load(song_path)
        mixer.music.play()
        self.volume = mixer.music.get_volume() * 100
        self.volume_scale.set(self.volume)
        
    # Play the song
    def play_song(self):

        # Check for paused song
        if mixer.music.get_busy() == False and mixer.music.get_pos() > 0:
            mixer.music.unpause()
            
        else:
            # Check for the command line argument, and plays the song
            try:
                mixer.music.load(sys.argv[1])
                mixer.music.play()
                self.volume = mixer.music.get_volume() * 100
                self.volume_scale.set(self.volume)
                self.add_song(sys.argv[1])

            # If no command line argument present, select file mannualy
            except:
                selected_song = self.playlist_box.curselection()
                if selected_song:
                    self.load_song(selected_song[0])
                    self.current_song_index = selected_song[0]

    # Play previous song
    def previous_song(self):
        self.current_song_index -= 1
        if (self.current_song_index < 0):
            self.current_song_index = len(self.playlist) - 1
            messagebox.showinfo("Error", "No previous song!")
        self.load_song(self.current_song_index)
        
    # Play next song
    def next_song(self):
        self.current_song_index += 1
        if (self.current_song_index > len(self.playlist) - 1):
            self.current_song_index = 0
            messagebox.showinfo("Error", "No next song!")
        try:
            self.load_song(self.current_song_index + 1)  
        except IndexError:
            messagebox.showinfo("Error", "No next song!")
    
    # keybord control
    def handle_key(self, event):
        if event.keysym == "Escape":
            self.stop_song()
        elif event.keysym == "Up" and self.volume < 100:
            self.set_volume(self.volume + 1)
        elif event.keysym == "Down" and self.volume > 0:
            self.set_volume(self.volume - 1)
        elif event.keysym == "Right":
            self.next_song()
        elif event.keysym == "Return":
            self.play_song()
        elif event.keysym == "Left":
            self.previous_song()
        elif event.keysym == "space":
            if mixer.music.get_busy() == False:
                self.play_song()
            else:
                self.pause_song()
        else:
            pass

    # Pause the song
    def pause_song(self):
        self.play_button.grid(row=0, column=3)
        if mixer.music.get_busy():
            self.play_button.grid(row=0, column=3)
            mixer.music.pause()

    # Set the volume
    def set_volume(self, value):
        self.volume = int(value)
        mixer.music.set_volume(self.volume / 100)
        self.volume_scale.set(self.volume)
    
    # Stops the song
    def stop_song(self):
        mixer.music.stop()

# Create the Tkinter window
root = Tk()

# Create the MusicPlayer object
music_player = MusicPlayer(root)
    
# Bind the key event to the player
root.bind("<Key>", music_player.handle_key)

# Run the Tkinter event loop
root.mainloop()
