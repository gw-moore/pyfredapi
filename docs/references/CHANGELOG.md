# Changelog

## Version 0.5.1 - 2022-11-5

### Added

- Support for python 3.11

### Removed

- Github actions for building docs

## Version 0.5.0 - 2022-10-26

This release introduces breaking changes. The `pyfredapi` api has been refactored to use functions rather than class methods

### Added

- CONTRIBUTING.md

### Changed

- Refactored the API into functions. Each FRED API endpoint now has an associated function rather than being attached to a class. All tests and docs have been updated to reflect this change
- Moved `SeriesData` to the `SeriesCollection` module. `get_series` now only returns series data. To get both series data and series info in
one object, use a `SeriesCollection`

### Fixed

- Broken formatting in the sphinx autodocs api reference

## Version 0.4.1 - 2022-10-20

### Changed

- Updated pydantic base model classes to accept extra parameters
- Updated `SeriesData.plot` x-axis label to include units
- Tweak docs formatting to adapt to sphinx_material theme

## Version 0.4.0 - 2022-10-19

### Added

- `SeriesCollection` class, test, and docs
- `plot` function to `SeriesData`
- Docstring to the top of all api modules

### Changed

- Sphinx docs theme to [sphinx_material](https://bashtage.github.io/sphinx-material/index.html)
- Removed 'dev' install group to make dependencies DRY
- Sonarcloud config to generate main branch statistics

## Version 0.3.0 - 2022-10-11

### Added

- Methods and tests for `FredRelease`, `FredTags`, and `FredSource`
- py.typed file
- Pull request template
- GitHub actions workflows for sonarcloud, linting, and testing

### Changed

- Updates `SeriesInfo`'s `notes` field to be optional
- Added `sort_order` parameter to `SeriesSearchParameters`
- Updates to the README
- Updates to the documentation

## Version 0.2.0 - 2022-09-27

### Added

- `SeriesData` class for the `get_series` methods. `SeriesData` holds both the data and the metadata for a given series.
- Unit tests for `FredSeries` method
- [vcr](https://vcrpy.readthedocs.io/en/latest/) pytest fixture to unit tests. vcr records the http interactions with the FRED api. Speeds up unit tests significantly and reduces the requests made to the FRED API
- `FredMaps` class and tests

### Changed

- Switch license to MIT
- Updates `FredCategory` & `FredSeries` method docstrings to fix typos, add missing parameters, and add links to the FRED endpoint documentation
- When returning data as a pandas dataframe, process the data so that date and numeric columns are the correct data type
- Renamed methods in `FredSeries`
  - `get_series_data` -> `get_series`
  - `get_series_data_all_releases` -> `get_series_all_releases`
  - `get_series_data_initial_release` -> `get_series_initial_release`
  - `get_series_data_asof_date` -> `get_series_asof_date`
- Rename `BaseApiArgs` to `BaseApiParameters`
- Rename `CategoryArgs` to `CategoryApiParameters`
- Rename `SeriesArgs` to `SeriesApiParameters`

### Fixed

- Install instructions
- pydantic dependency
- `FredSeries.get_series_releases` endpoint
- Removed `series_id` from `SeriesArgs`

## Version 0.1.0 - 2022-09-25

**Note:** This version has been deleted from pypi

Initial release of `pyfredapi` package

### Added

- `FredApi` class
- `FredCategory` class
- `FredSeries` class
- `FredMaps` stub
- `FredSources` stub
- `FredTags` stub
- Sphinx docs
