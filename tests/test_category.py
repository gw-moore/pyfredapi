import pandas as pd
import pytest

from pyfredapi.category import (
    get_category,
    get_category_children,
    get_category_related,
    get_category_related_tags,
    get_category_series,
    get_category_tags,
)
from pyfredapi.series import SeriesInfo

from .conftest import get_request as category_request

category_params = {
    "category_id": 125,
}


@pytest.mark.vcr()
def test_get_category():
    actual = get_category(category_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)

    expected = category_request(
        endpoint="category", extra_params=category_params
    ).json()
    assert expected == actual


@pytest.mark.vcr()
def test_get_category_children():
    actual = get_category_children(category_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)

    expected = category_request(
        endpoint="category/children", extra_params=category_params
    ).json()
    assert expected == actual


@pytest.mark.vcr()
def test_get_category_related():
    actual = get_category_related(category_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)

    expected = category_request(
        endpoint="category/related", extra_params=category_params
    ).json()
    assert expected == actual


@pytest.mark.vcr()
def test_get_category_series():
    actual = get_category_series(category_id=category_params["category_id"])
    expected = category_request(
        endpoint="category/series", extra_params=category_params
    ).json()

    expected = {series["id"]: SeriesInfo(**series) for series in expected["seriess"]}

    assert isinstance(actual, dict)
    for series_info in actual.values():
        assert isinstance(series_info, SeriesInfo)
    assert actual == expected


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_category_tags(return_type):
    actual = get_category_tags(
        category_id=category_params["category_id"],
        return_format=return_type,
    )
    expected = category_request(
        endpoint="category/tags", extra_params=category_params
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "tags" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(pd.DataFrame.from_dict(expected["tags"]), actual)


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_category_related_tags(return_type):
    actual = get_category_related_tags(
        category_id=category_params["category_id"],
        return_format=return_type,
        **{"tag_names": "balance"},
    )

    expected = category_request(
        endpoint="category/related_tags",
        extra_params={**category_params, "tag_names": "balance"},
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "tags" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(pd.DataFrame.from_dict(expected["tags"]), actual)
