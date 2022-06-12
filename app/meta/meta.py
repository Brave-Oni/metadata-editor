import os
from exif import Image


class MetaImage:
    PATH = "app/upload/"
    METAS = [
        "make",
        "model",
        "datetime",
        "gps_latitude",
        "gps_longitude",
        "gps_latitude_ref",
        "gps_longitude_ref"
    ]

    def __init__(self, filename):
        with open(os.path.join(self.PATH, filename), "rb") as image_file:
            self.image = Image(image_file)

    def get_metadata(self):
        return {
            key: self.image.get(key, None) for key in self.METAS
        } if self.image.has_exif else None

    def set_metadata(self, attr, value):
        self.image[attr] = value

    @staticmethod
    def to_decimal_degree(dms, ref):
        dd = sum(x / 60**i for i, x in enumerate(dms))
        return -dd if ref == "S" or ref == "W" else dd

    @staticmethod
    def to_degree_minutes_seconds(dd):
        degree = int(dd)
        minutes = int((dd - degree) * 60)
        seconds = (dd - degree - minutes / 60) * 3600
        return degree, minutes, seconds

    def save(self, filename):
        with open(os.path.join(self.PATH, filename), "wb") as image_file:
            image_file.write(self.image.get_file())
