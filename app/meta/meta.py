import os
from exif import Image
import exifread
from geopy.geocoders import Nominatim


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
        self.filename = filename
        with open(os.path.join(self.PATH, filename), "rb") as image_file:
            self.image = Image(image_file)

    def get_metadata(self):
        return {
            key: self.image.get(key, None) for key in self.METAS
        } if self.image.has_exif else None

    def set_metadata(self, attr, value):
        self.image[attr] = value

    def __format_latitude_longitude(self, data):
        list_tmp = str(data).replace('[', '').replace(']', '').split(',')
        list = [ele.strip() for ele in list_tmp]
        print(list)
        if list[-1].find('/') != -1:
            data_sec = int(list[-1].split('/')[0]) / (int(list[-1].split('/')[1]) * 3600)
        else:
            data_sec = int(list[-1]) / 3600

        data_minute = int(list[2]) / 60
        data_degree = int(list[0])
        result = data_degree + data_minute + data_sec
        return result

    def get_location(self):
        try:
            img = exifread.process_file(open(os.path.join(self.PATH, self.filename), 'rb'))
            latitude = self.__format_latitude_longitude(str(img['GPS GPSLatitude']))
            longitude = self.__format_latitude_longitude(str(img['GPS GPSLongitude']))
            geolocator = Nominatim(user_agent="your email")
            position = geolocator.reverse(str(latitude) + ',' + str(longitude))
            return position.address
        except KeyError:
            return "No info"

    def save(self, filename):
        with open(os.path.join(self.PATH, filename), "wb") as image_file:
            image_file.write(self.image.get_file())
