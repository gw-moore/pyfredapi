import pkg_resources as _pkg_resources

__version__ = _pkg_resources.get_distribution("pyfredapi").version

from .api import FredApi, FredCategory, FredSeries, ReturnFormat
