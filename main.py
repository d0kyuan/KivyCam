#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: test123.py
# Project: Desktop
# Created Date: Tuesday, October 6th 2020, 11:07:19 pm
# Author: Ray
# -----
# Last Modified: Sunday, October 11th 2020, 9:54:17 pm
# Modified By: Ray
# -----
# Copyright (c) 2020 Ray
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###
try:
    from android.permissions import request_permissions, Permission

except:
    pass
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
import os
import sys
from datetime import datetime
if getattr(sys, 'frozen', False):
    os.environ["root"] = sys._MEIPASS
elif __file__:
    os.environ["root"] = os.path.abspath(".")


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Teal"
        self.dialog_change_theme = None
        self.toolbar = None
        self.data_screens = {}

    def build(self):
        try:

            request_permissions(
                [Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE])
        except:
            pass

        Builder.load_file(f"{os.environ['root']}/screen/HomePage.kv")
        return Builder.load_file(f"{os.environ['root']}/main.kv")

    def back_to_home_screen(self):
        self.root.ids.screen_manager.current = "homepage"


if __name__ == '__main__':
    MyApp().run()
