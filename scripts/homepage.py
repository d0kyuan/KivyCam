#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: homepage.py
# Project: scripts
# Created Date: Friday, October 9th 2020, 1:09:27 am
# Author: Ray
# -----
# Last Modified:
# Modified By:
# -----
# Copyright (c) 2020 Ray
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###
from android import activity, mActivity
import time
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from os import getcwd
from datetime import datetime
from os.path import exists
from kivymd.toast import toast
from jnius import autoclass, cast
from kivy.uix.image import Image, CoreImage
from kivy.clock import Clock
import android
import android.activity
Uri = autoclass('android.net.Uri')
String = autoclass('java.lang.String')
Intent = autoclass('android.content.Intent')
MediaStore = autoclass('android.provider.MediaStore')
Environment = autoclass('android.os.Environment')
Context = autoclass("android.content.Context")
FileProvider = autoclass('android.support.v4.content.FileProvider')
PythonActivity = autoclass("org.kivy.android.PythonActivity").mActivity


class HomePage(Screen):
    filepath = ""

    def capture(self):
        def create_img_file():
            File = autoclass('java.io.File')
            storageDir = Context.getExternalFilesDir(
                Environment.DIRECTORY_PICTURES)

            imageFile = File(
                storageDir,
                f"{int(datetime.now().timestamp())}.png"
            )
            imageFile.createNewFile()
            return imageFile
        android.activity.unbind(on_activity_result=self._on_activity_result)
        android.activity.bind(on_activity_result=self._on_activity_result)
        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)

        photoFile = create_img_file()
        self.filepath = photoFile.getAbsolutePath()
        photoUri = FileProvider.getUriForFile(
            Context.getApplicationContext(),
            "com.heattheatr.kitchen_sink.fileprovider",
            photoFile
        )

        parcelable = cast('android.os.Parcelable', photoUri)

        intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)
        mActivity.startActivityForResult(intent, 0x123)
        # try:

        #     camera.take_picture(filename=self.filepath,
        #                         on_complete=self.camera_callback)
        # except NotImplementedError:
        #     toast(
        #         "This feature has not yet been implemented for this platform.")
    def _on_activity_result(self, requestCode, resultCode, intent):

        if requestCode != 0x123:
            return
        android.activity.unbind(on_activity_result=self._on_activity_result)
        Clock.schedule_once(self.changeImage, 3)

    def camera_callback(self, filepath, byteData):
        print("filepath", filepath)
        self.filepath = filepath

    def changeImage(self, dt):
        self.ids.imageView.source = self.filepath

    def upload(self):
        pass
