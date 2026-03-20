import customtkinter as ctk
from tkinter import filedialog
import pygame
import numpy as np
import threading
import time
import os
import math

pygame.mixer.init()

class AudioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Audio Player")
        self.root.geometry("900x600")

        self.playlist = []
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.audio_data = None
        self.sample_rate = 44100
        self.track_length = 0
        self.rotation = 0

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

        self.playlist_box = ctk.CTkTextbox(root, width=250, height=550)
        self.playlist_box.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.label = ctk.CTkLabel(root, text="Keine Datei geladen", font=("Arial", 18))
        self.label.grid(row=0, column=1, pady=(10, 0))

        self.button_frame = ctk.CTkFrame(root)
        self.button_frame.grid(row=1, column=1, pady=10)

        self.load_btn = ctk.CTkButton(self.button_frame, text="Dateien hinzufügen", command=self.load_files)
        self.load_btn.grid(row=0, column=0, padx=5)

        self.play_btn = ctk.CTkButton(self.button_frame, text="Play / Pause", command=self.play_pause)
        self.play_btn.grid(row=0, column=1, padx=5)

        self.stop_btn = ctk.CTkButton(self.button_frame, text="Stop", command=self.stop)
        self.stop_btn.grid(row=0, column=2, padx=5)

        self.volume_slider = ctk.CTkSlider(root, from_=0, to=1, command=self.set_volume, width=300)
        self.volume_slider.set(0.5)
        pygame.mixer.music.set_volume(0.5)
        self.volume_slider.grid(row=2, column=1, pady=10)

        self.progress_label = ctk.CTkLabel(root, text="00:00 / 00:00")
        self.progress_label.grid(row=3, column=1)

        self.canvas = ctk.CTkCanvas(root, width=600, height=300, bg="#111111", highlightthickness=0)
        self.canvas.grid(row=4, column=1, pady=10)

        threading.Thread(target=self.update_progress, daemon=True).start()
        threading.Thread(target=self.update_visualizer, daemon=True).start()

    def load_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if not files:
            return
        for f in files:
            p = os.path.abspath(f)
            self.playlist.append(p)
            self.playlist_box.insert("end", os.path.basename(p) + "\n")
        if self.current_index == -1:
            self.current_index = 0
            self.load_track(0)

    def load_track(self, index):
        file = self.playlist[index]
        pygame.mixer.music.load(file)
        snd = pygame.mixer.Sound(file)
        arr = pygame.sndarray.array(snd).astype(np.float32)
        if len(arr.shape) == 2:
            arr = arr.mean(axis=1)
        self.audio_data = arr
        self.sample_rate = snd.get_length() and int(len(arr) / snd.get_length())
        self.track_length = len(arr) / self.sample_rate
        self.label.configure(text=os.path.basename(file))
        self.is_playing = False
        self.is_paused = False

    def play_pause(self):
        if self.current_index == -1:
            return
        if not self.is_playing:
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            return
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False

    def set_volume(self, v):
        pygame.mixer.music.set_volume(float(v))

    def update_progress(self):
        while True:
            if self.is_playing and not self.is_paused:
                pos = pygame.mixer.music.get_pos() / 1000
                if pos >= self.track_length - 0.5:
                    self.next_track()
                self.progress_label.configure(text=self.format_time(pos) + " / " + self.format_time(self.track_length))
            time.sleep(0.2)

    def update_visualizer(self):
        while True:
            if self.is_playing and not self.is_paused and self.audio_data is not None:
                pos = pygame.mixer.music.get_pos() / 1000
                idx = int(pos * self.sample_rate)
                window = self.audio_data[idx:idx + 2048]
                if len(window) < 2048:
                    self.canvas.delete("all")
                    time.sleep(0.03)
                    continue
                fft = np.abs(np.fft.rfft(window))[:80]
                self.canvas.delete("all")
                cx, cy = 300, 150
                radius = 60
                angle_step = 2 * math.pi / len(fft)
                self.rotation += 0.02
                for i, v in enumerate(fft):
                    h = min(100, v / 1500)
                    angle = i * angle_step + self.rotation
                    x0 = cx + math.cos(angle) * radius
                    y0 = cy + math.sin(angle) * radius
                    x1 = cx + math.cos(angle) * (radius + h)
                    y1 = cy + math.sin(angle) * (radius + h)
                    self.canvas.create_line(x0, y0, x1, y1, fill="#00aaff", width=3)
            time.sleep(0.03)

    def next_track(self):
        if self.current_index + 1 < len(self.playlist):
            self.current_index += 1
            self.load_track(self.current_index)
            pygame.mixer.music.play()
        else:
            self.stop()

    def format_time(self, sec):
        sec = int(sec)
        return f"{sec//60:02d}:{sec%60:02d}"


ctk.set_appearance_mode("dark")
root = ctk.CTk()
app = AudioPlayer(root)
root.mainloop()
