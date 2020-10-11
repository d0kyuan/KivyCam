import android
import android.activity
from os import remove
from jnius import autoclass, cast
from plyer.facades import Camera
from plyer.platforms.android import activity
from datetime import datetime
Intent = autoclass('android.content.Intent')
MediaStore = autoclass('android.provider.MediaStore')
Uri = autoclass('android.net.Uri')
File = autoclass('java.io.File')
ByteArrayOutputStream = autoclass('java.io.ByteArrayOutputStream')
CompressFormat = autoclass('android.graphics.Bitmap$CompressFormat')
FileOutputStream = autoclass('java.io.FileOutputStream')


class AndroidCamera(Camera):

    def _take_picture(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        android.activity.unbind(on_activity_result=self._on_activity_result)
        android.activity.bind(on_activity_result=self._on_activity_result)
        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        folder = File("/storage/emulated/0/", "rayyuan")
        if not folder.exists():
            folder.mkdirs()
        filename2 = str(int(datetime.now().timestamp()))+"AA.png"
        # f = File("/storage/emulated/0/rayyuan",
        #          filename2)
        # f.createNewFile()
        # mImageUri = Uri.fromFile(f)
        uri = Uri.parse(f"content://storage/emulated/0/rayyuan/{filename2}")
        # # imageUri = Uri.fromfile(f)
        # print(type(mImageUri))
        print(uri)
        parcelable = cast('android.os.Parcelable', uri)
        # intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable
        #                 )
        activity.startActivityForResult(intent, 0x123)

    def _take_video(self, on_complete, filename=None):
        assert(on_complete is not None)
        self.on_complete = on_complete
        self.filename = filename
        android.activity.unbind(on_activity_result=self._on_activity_result)
        android.activity.bind(on_activity_result=self._on_activity_result)
        intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
        # uri = Uri.parse('file://' + filename)
        # parcelable = cast('android.os.Parcelable', uri)
        # intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)

        # 0 = low quality, suitable for MMS messages,
        # 1 = high quality
        intent.putExtra(MediaStore.EXTRA_VIDEO_QUALITY, 1)
        activity.startActivityForResult(intent, 0x123)

    def _on_activity_result(self, requestCode, resultCode, intent):

        if requestCode != 0x123:
            return
        android.activity.unbind(on_activity_result=self._on_activity_result)
        extras = intent.getExtras()
        folder = File("/storage/emulated/0/", "rayyuan")
        if not folder.exists():
            folder.mkdirs()
        filename = str(int(datetime.now().timestamp()))+".png"
        filename2 = str(int(datetime.now().timestamp()))+"AA.png"
        f = File("/storage/emulated/0/rayyuan",
                 filename)
        f.createNewFile()
        bitmap = extras.get("data")
        bos = ByteArrayOutputStream()

        fOut = FileOutputStream(f)

        bitmap.compress(CompressFormat.PNG, 85, fOut)
        fOut.flush()
        fOut.close()
        # bitmap.compress(CompressFormat.PNG, 100, bos)
        # Bitmap b = BitmapFactory.decodeByteArray(imageAsBytes, 0, imageAsBytes.length)
        # profileImage.setImageBitmap();
        bitmapdata = bos.toByteArray()
        # fos = FileOutputStream(f)
        # fos.write(bitmapdata)
        # fos.flush()
        # fos.close()
        #
        # print(extras.get("data")
        #       )
        # print(type(dir(extras.get("data"))))
        # print(dir(extras.get("data")))
        self.on_complete(
            f"/storage/emulated/0/rayyuan/{filename}", bitmapdata)
        #     self._remove(self.filename

    def _remove(self, fn):
        try:
            remove(fn)
        except OSError:
            pass


def instance():
    return AndroidCamera()
