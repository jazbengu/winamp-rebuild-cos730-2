import os
import pygame
from tkinter import Tk, Button, Label, filedialog, Scale
from tkinter.ttk import Progressbar

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Winamp")
        self.root.geometry("400x250")
        self.playlist = []
        self.current_track_index = 0

        self.play_btn = Button(root, text="Play", bg="lightgray", fg="black", width=5, command=self.play)
        self.play_btn.grid(row=0, column=0, padx=5, pady=5)

        self.pause_btn = Button(root, text="Pause", bg="lightgray", fg="black", width=5, command=self.pause)
        self.pause_btn.grid(row=0, column=1, padx=5, pady=5)

        self.stop_btn = Button(root, text="Stop", bg="lightgray", fg="black", width=5, command=self.stop)
        self.stop_btn.grid(row=0, column=2, padx=5, pady=5)

        self.next_btn = Button(root, text="Next", bg="lightgray", fg="black", width=5, command=self.next_track)
        self.next_btn.grid(row=0, column=3, padx=5, pady=5)

        self.prev_btn = Button(root, text="Previous", bg="lightgray", fg="black", width=5, command=self.prev_track)
        self.prev_btn.grid(row=0, column=4, padx=5, pady=5)

        self.load_btn = Button(root, text="Load Playlist", bg="lightgray", fg="black", width=10, command=self.load_playlist)
        self.load_btn.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

        self.current_track_label = Label(root, text="", bg="lightgray", fg="black", width=40)
        self.current_track_label.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

        self.volume_label = Label(root, text="Volume:", bg="lightgray", fg="black")
        self.volume_label.grid(row=3, column=0, padx=5, pady=5)

        self.volume_slider = Scale(root, from_=0, to=100, orient="horizontal", length=150, bg="lightgray", fg="black", command=self.set_volume)
        self.volume_slider.set(70)  # Default volume level
        self.volume_slider.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        self.progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=4, column=0, columnspan=5, padx=5, pady=5)

    def load_playlist(self):
        self.playlist = filedialog.askopenfilenames()
        if self.playlist:
            self.current_track_index = 0
            self.play_current_track()

    def play_current_track(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.playlist[self.current_track_index])
        pygame.mixer.music.play()
        self.update_current_track_label()
        self.update_progress_bar()

    def update_current_track_label(self):
        current_track = os.path.basename(self.playlist[self.current_track_index])
        self.current_track_label.config(text="Now Playing: " + current_track)

    def update_progress_bar(self):
        total_length = pygame.mixer.Sound(self.playlist[self.current_track_index]).get_length()
        self.progress_bar.config(maximum=total_length)
        self.check_progress()

    def check_progress(self):
        current_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
        self.progress_bar.config(value=current_time)
        self.progress_bar.after(100, self.check_progress)

    def set_volume(self, val):
        volume = int(val) / 100
        pygame.mixer.music.set_volume(volume)

    def play(self):
        pygame.mixer.music.unpause()

    def pause(self):
        pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.music.stop()

    def next_track(self):
        if self.current_track_index < len(self.playlist) - 1:
            self.current_track_index += 1
            self.play_current_track()

    def prev_track(self):
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.play_current_track()

if __name__ == "__main__":
    root = Tk()
    root.configure(bg="lightgray")
    music_player = MusicPlayer(root)
    root.mainloop()
