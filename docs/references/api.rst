pyfredapi: Public API Reference
================================

FRED Categories
------------------------------
.. currentmodule:: pyfredapi.category
.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    get_category
    get_category_children
    get_category_related
    get_category_related_tags
    get_category_series
    get_category_tags
    CategoryApiParameters

FRED Maps
------------------------------
.. currentmodule:: pyfredapi.maps
.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    get_geoseries
    get_geoseries_info
    get_shape_files
    MapApiParameters

FRED Series
------------------------------
.. currentmodule:: pyfredapi.series
.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    get_series
    get_series_all_releases
    get_series_asof_date
    get_series_categories
    get_series_info
    get_series_initial_release
    get_series_releases
    get_series_tags
    get_series_updates
    get_series_vintagedates
    search_series
    search_series_related_tags
    search_series_tags
    SeriesApiParameters
    SeriesInfo
    SeriesSearchParameters

FRED Sources
------------------------------
.. currentmodule:: pyfredapi.sources
.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    get_sources
    get_source
    get_source_release
    SourceApiParameters

FRED Tags
------------------------------
.. currentmodule:: pyfredapi.tags
.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    get_tags
    get_related_tags
    get_series_matching_tags
    TagsApiParameters

Series Collection
------------------------------
.. currentmodule:: pyfredapi.series_collection
.. autosummary::
    :toctree: _autosummary
    :nosignatures:

    SeriesCollection
    SeriesData