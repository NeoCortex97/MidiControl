#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import pygame.time as time
import pathlib


class Button:
    def __init__(self, path, loop, volume, fadetime):
        if not pygame.get_init():
            pygame.init()
            pygame.mixer.init()
        self.sound = pygame.mixer.Sound(str(pathlib.Path(path).expanduser()))
        self.sound.set_volume(volume)
        self.loop = loop
        self.fade_time = fadetime
        self.playing = False

    def play(self):
        print("[INFO] Starteing Sound")
        if self.loop:
            self.sound.play(loops=-1, fade_ms=self.fade_time)
        else:
            self.sound.play(fade_ms=self.fade_time)
        self.playing = True

    def stop(self):
        print("[INFO] Stopping Sound")
        self.sound.fadeout(self.fade_time)
        self.playing = False

    def toggle(self):
        if not self.playing:
            print("[DEBUG] Calling play")
            self.play()
        else:
            print("[DEBUG] Calling stop")
            self.stop()


def main(**kwargs):
    pygame.init()
    pygame.mixer.init()
    files = ["file1.wav",
             "file2.wav"]
    buttons = []
    for item in files:
        buttons.append(Button(item, True, 0.5, 1000))

    buttons[0].toggle()
    time.wait(5000)
    buttons[0].toggle()


if __name__ == "__main__":
    main()