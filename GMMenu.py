#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import pygame
from pygame import time
import launchpad_py as launchpad
import pathlib


class Button:
    def __init__(self, path, name, x, y, color, loop, volume, fadetime):
        if not pygame.get_init():
            pygame.init()
            pygame.mixer.init()
        self.sound = pygame.mixer.Sound(str(pathlib.Path(path).expanduser()))
        self.sound.set_volume(volume)
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.loop = loop
        self.fade_time = fadetime
        self.playing = False

    def light(self):
        return self.x, self.y, self.color

    def play(self):
        print("[INFO] Started {}".format(self.name))
        if self.loop:
            self.sound.play(loops=-1, fade_ms=self.fade_time)
        else:
            self.sound.play(fade_ms=self.fade_time)
        self.playing = True

    def stop(self):
        print("[INFO] Stopping {}".format(self.name))
        self.sound.fadeout(self.fade_time)
        self.playing = False

    def toggle(self):
        if not self.playing:
            print("[DEBUG] Calling play")
            self.play()
        else:
            print("[DEBUG] Calling stop")
            self.stop()

    def __eq__(self, other):
        if (type(other) == list) and (len(other) == 3):
            for item in other:
                if type(item) != int:
                    return False
            return (self.x == other[0]) and (self.y == other[1]) and (other[2] > 0)
        else:
            return False

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.color
        elif item == 3:
            return self.name
        else:
            raise IndexError("Object index out of range")


class Controller:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()
            pygame.mixer.init()
        self.running = True
        self.need_redraw = True
        self.lp = launchpad.LaunchpadMk2()
        if self.lp.Open(0, "mk2"):
            print("[INFO] Opened Launchpad mk2")
        else:
            print("[ERROR] Cound not find a Launchpad!")
            return
        self.lp.ButtonFlush()
        self.lp.LedAllOn(0)
        print("[INFO] Loading settings . . .")
        self.data = json.load(open("settings.json", "r", encoding="utf-8"))
        self.mode = self.data["default_mode"]
        self.music_page = self.data["music"]["default_page"]
        self.music_mode_button = (self.data["music"]["pages"][str(self.music_page)]["button_x"],
                                    self.data["music"]["pages"][str(self.music_page)]["button_y"],
                                    self.data["music"]["pages"][str(self.music_page)]["button_color"])
        self.pages = [[]]
        print("[INFO] Loading music files . . .")
        for item in self.data["music"]["pages"][str(self.music_page)]["songs"]:
            self.pages[-1].append(Button(self.data["music"]["directory"] + item["file"],item["name"], item["x"], item["y"], item["color"], item["loop"], item["volume"], 1000))

    def mainlooop(self):
        while self.running:
            if self.need_redraw:
                if self.mode == "music":
                    self.lp.LedCtrlXYByCode(4, 0, 17)
                    for i in range(5, 8):
                        self.lp.LedCtrlXYByCode(i, 0, 1)
                    for i in range(1, 9):
                        self.lp.LedCtrlXYByCode(8, i, 1)
                    self.lp.LedCtrlXYByCode(self.music_mode_button[0], self.music_mode_button[1], self.music_mode_button[2])

                    for item in self.pages[-1]:
                        self.lp.LedCtrlXYByCode(item[0], item[1], item[2])
                self.need_redraw = False
            button = self.lp.ButtonStateXY()
            while button != []:
                for b in self.pages[-1]:
                    if b == button:
                        b.toggle()
                        break
                button = self.lp.ButtonStateXY()


def main(**kwargs):
    mod = Controller()
    mod.mainlooop()


if __name__ == "__main__":
    main()
