import os

class FileUtil():
    @classmethod
    def get_image_full_path(cls, img_path):
        return os.path.abspath(img_path)
