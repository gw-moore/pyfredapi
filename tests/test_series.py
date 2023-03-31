import pandas as pd
import pytest

from pyfredapi.series import (
    SeriesInfo,
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
from pyfredapi.utils import _convert_to_pandas

from .conftest import get_request

series_params = {
    "series_id": "GDP",
}

test_search_text = "monetary+service+index"
series_obv_endpoint = "series/observations"

return_type_mark = pytest.mark.parametrize("return_type", ["json", "pandas"])


@pytest.mark.vcr()
def test_get_series_info():
    actual = get_series_info(series_params["series_id"])
    assert isinstance(actual, SeriesInfo)


@pytest.mark.vcr()
def test_get_series_categories():
    actual = get_series_categories(series_id=series_params["series_id"])
    expected = get_request(
        endpoint="series/categories",
        extra_params=series_params,
    ).json()
    assert isinstance(actual, dict)
    assert expected == actual


@pytest.mark.vcr()
@return_type_mark
def test_get_series(return_type):
    actual = get_series(series_id=series_params["series_id"], return_format=return_type)
    expected = get_request(
        endpoint=series_obv_endpoint, extra_params=series_params
    ).json()["observations"]

    if return_type == "json":
        assert isinstance(actual, list)
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected), actual)


@pytest.mark.vcr()
def test_get_series_releases():
    actual = get_series_releases(series_id=series_params["series_id"])
    expected = get_request(
        endpoint="series/release",
        extra_params=series_params,
    ).json()
    assert isinstance(actual, dict)
    assert expected == actual


@pytest.mark.vcr()
def test_get_series_tags():
    actual = get_series_tags(series_id=series_params["series_id"])
    expected = get_request(
        endpoint="series/tags",
        extra_params=series_params,
    ).json()
    assert isinstance(actual, dict)
    assert expected == actual


@pytest.mark.vcr()
def test_get_series_updates():
    actual = get_series_updates(series_id=series_params["series_id"])
    expected = get_request(
        endpoint="series/updates",
        extra_params=series_params,
    ).json()
    assert isinstance(actual, dict)
    assert expected == actual


@pytest.mark.vcr()
def test_get_series_vintagedates():
    actual = get_series_vintagedates(series_id=series_params["series_id"])
    expected = get_request(
        endpoint="series/vintagedates",
        extra_params=series_params,
    ).json()["vintage_dates"]
    assert isinstance(actual, list)
    assert expected == actual


@pytest.mark.vcr()
@return_type_mark
def test_get_series_all_releases(return_type):
    actual = get_series_all_releases(
        series_id=series_params["series_id"], return_format=return_type
    )

    expected = get_request(
        endpoint=series_obv_endpoint,
        extra_params={
            "realtime_start": "1776-07-04",
            "realtime_end": "9999-12-31",
            "series_id": series_params["series_id"],
        },
    ).json()["observations"]

    if return_type == "json":
        assert isinstance(actual, list)
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected), actual)


@pytest.mark.vcr()
@return_type_mark
def test_get_series_initial_release(return_type):
    actual = get_series_initial_release(
        series_id=series_params["series_id"], return_format=return_type
    )

    expected = get_request(
        endpoint=series_obv_endpoint,
        extra_params={
            "realtime_start": "1776-07-04",
            "output_type": "4",
            "series_id": series_params["series_id"],
        },
    ).json()["observations"]

    if return_type == "json":
        assert isinstance(actual, list)
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected), actual)


@pytest.mark.vcr()
@return_type_mark
def test_get_series_asof_date(return_type):
    actual = get_series_asof_date(
        series_id=series_params["series_id"],
        date="2019-01-01",
        return_format=return_type,
    )

    expected = get_request(
        endpoint=series_obv_endpoint,
        extra_params={
            "realtime_start": "1776-07-04",
            "realtime_end": "2019-01-01",
            "series_id": series_params["series_id"],
        },
    ).json()["observations"]

    if return_type == "json":
        assert isinstance(actual, list)
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected), actual)


@pytest.mark.vcr()
@return_type_mark
def test_search_series(return_type):
    actual = search_series(
        search_text=test_search_text,
        return_format=return_type,
    )
    expected = get_request(
        endpoint="series/search",
        extra_params={
            "search_text": test_search_text,
            "search_type": "full_text",
        },
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "seriess" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected["seriess"]), actual)


@pytest.mark.vcr()
@return_type_mark
def test_search_series_tags(return_type):
    actual = search_series_tags(
        search_text=test_search_text,
        return_format=return_type,
    )
    expected = get_request(
        endpoint="series/search/tags",
        extra_params={"series_search_text": test_search_text},
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "tags" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected["tags"]), actual)


@pytest.mark.vcr()
@return_type_mark
def test_search_series_related_tags(return_type):
    actual = search_series_related_tags(
        search_text=test_search_text,
        tag_names="30-year;frb",
        return_format=return_type,
    )
    expected = get_request(
        endpoint="series/search/related_tags",
        extra_params={
            "series_search_text": test_search_text,
            "tag_names": "30-year;frb",
        },
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "tags" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(_convert_to_pandas(expected["tags"]), actual)
