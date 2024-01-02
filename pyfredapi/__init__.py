"""pyfredapi - Python client for the Federal Reserve Economic Data (FRED) API
==============================================================================.

**pyfredapi** is a Python client for the FRED API web service (https://fred.stlouisfed.org/docs/api/fred/).
`pyfredapi` covers all the FRED API endpoints and can return data as a pandas (https://pandas.pydata.org/)
dataframe or json. Checkout the [docs](https://pyfredapi.readthedocs.io/en/latest/) to learn more.
"""

from importlib.metadata import version as _version

__version__ = _version("pyfredapi")

from .category import (
    CategoryApiParameters,
    get_category,
    get_category_children,
    get_category_related,
    get_category_related_tags,
    get_category_series,
    get_category_tags,
)
from .maps import MapApiParameters, get_geoseries, get_geoseries_info, get_shape_files
from .releases import (
    ReleaseApiParameters,
    get_release,
    get_release_dates,
    get_release_related_tags,
    get_release_series,
    get_release_sources,
    get_release_tables,
    get_release_tags,
    get_releases,
    get_releases_dates,
)
from .series import (
    SeriesApiParameters,
    SeriesInfo,
    SeriesSearchParameters,
    get_series,
    get_series_all_releases,
    get_series_asof_date,
    get_series_categories,
    get_series_info,
    get_series_initial_release,
    get_series_releases,
    get_series_tags,
    get_series_updates,
    get_series_vintagedates,
    search_series,
    search_series_related_tags,
    search_series_tags,
)
from .series_collection import SeriesCollection, SeriesData
from .sources import SourceApiParameters, get_source, get_source_release, get_sources
from .tags import (
    TagsApiParameters,
    get_related_tags,
    get_series_matching_tags,
    get_tags,
)
