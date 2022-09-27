# Changelog

## Version 0.2.0

### Added

- `SeriesData` class for the `get_series` methods. `SeriesData` holds both the data and the metadata for a given series.
- Unit tests for FredSeries method.
- [vcr](https://vcrpy.readthedocs.io/en/latest/) pytest fixture to unit tests. vcr records the http interactions with the FRED api. Speeds up unit tests significantly and reduces the requests made to the FRED api.
- `FredMaps` class and tests.

### Changed

- Switch license to MIT.
- Updates FredCategory & FredSeries method docstrings to fix typos, add missing parameters, and add links to the FRED endpoint documentation.
- Process data when returning pandas data so that date and numeric columns are the correct type.
- FredSeries.get_series_all_releases changed to FredSeries.get_series_data_all_releases.
- FredSeries.get_series_initial_release to FredSeries.get_series_data_initial_release.
- FredSeries.get_series_asof_date to FredSeries.get_series_data_asof_date.
- Rename BaseApiArgs to BaseApiParameters.
- Rename CategoryArgs to CategoryApiParameters.
- Rename SeriesArgs to SeriesApiParameters.

### Fixed

- FredSeries.get_series_releases endpoint.

## Version 0.1.0post2 - 2022-09-26

- Fix install instructions.

## Version 0.1.0post1 - 2022-09-25

**Note:** This version has been yanked from pypi.

### Fixed

- Removed `series_id` from `SeriesArgs`.

## Version 0.1.0post0 - 2022-09-25

**Note:** This version has been yanked from pypi.

### Fixed

- Fixes pydantic dependency.

## Version 0.1.0 - 2022-09-25

**Note:** This version has been deleted from pypi.

Initial release of `pyfredapi` package.

### Added

- FredApi class
- FredCategory class
- FredSeries class
- FredMaps stub
- FredSources stub
- FredTags stub
- Sphinx docs