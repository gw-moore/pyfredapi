from .base import ReturnFormat
from .category import FredCategory
from .maps import FredMaps
from .releases import FredRelease
from .series import FredSeries
from .sources import FredSources
from .tags import FredTags


class FredApi(FredCategory, FredMaps, FredRelease, FredSeries, FredSources, FredTags):
    pass
