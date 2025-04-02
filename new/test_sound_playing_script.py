from tkinter import *
import pygame

root = Tk()
root.title('SONG PLAYING MODULE')
root.geometry('500x400')

pygame.mixer.init()

def play():
    try:
        pygame.mixer.music.load("new\\audio_tracks\\superstition.mp3")
        print("MP3 file loaded successfully!")
        pygame.mixer_music.play()
    except pygame.error as e:
        print("Error loading file:", e)

my_button = Button(root, text="play", command=lambda: play())
my_button.pack(pady=20)


root.mainloop()