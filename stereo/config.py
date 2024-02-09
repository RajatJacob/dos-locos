import json
from enum import Enum
from pathlib import Path


class StereoImageConfig(Enum):
    SATELLITE = 'satellite'
    CORRIDOR = 'corridor'
    PASSAU = 'passau'
    BUILDING = 'building'
    PARKING = 'parking'
    MOON = 'moon'
    SNOW = 'snow'
    NEBULA = 'nebula'
    PENTAGON = 'pentagon'
    BUG = 'bug'

    @property
    def config(self):
        if not (hasattr(self, '__config') and self.__config is not None):
            self.__config = json.load(
                open(Path(__file__).parent / 'stereo_config.json', 'r'))[self.value]
        return self.__config

    @property
    def filename(self):
        """Returns the filename of the image."""
        return str(self.config['filename'])

    @property
    def lOffset(self):
        """Returns the number of pixels to be cropped from the left."""
        return int(self.config.get('lOffset', 0))

    @property
    def rOffset(self):
        """Returns the number of pixels to be cropped from the right."""
        return int(self.config.get('rOffset', 0))

    @property
    def block_size(self):
        return int(self.config.get('blockSize', 5))
