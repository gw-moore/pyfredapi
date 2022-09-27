from .base import ReturnFormat
from .category import FredCategory
from .maps import FredMaps
from .series import FredSeries
from .sources import FredSources
from .tags import FredTags


class FredApi(FredCategory, FredSeries):
    pass
