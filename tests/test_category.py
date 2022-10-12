import pandas as pd
import pytest

from pyfredapi import FredCategory
from pyfredapi.api.utils import _convert_to_pandas

from .conftest import base_request as category_request

category_params = {
    "category_id": 125,
}


@pytest.fixture()
def client():
    return FredCategory()


@pytest.mark.vcr()
def test_get_category(client):
    actual = client.get_category(category_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)

    expected = category_request(
        endpoint="category", extra_params=category_params
    ).json()
    assert expected == actual


@pytest.mark.vcr()
def test_get_category_children(client):
    actual = client.get_category_children(category_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)

    expected = category_request(
        endpoint="category/children", extra_params=category_params
    ).json()
    assert expected == actual


@pytest.mark.vcr()
def test_get_category_related(client):
    actual = client.get_category_related(category_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)

    expected = category_request(
        endpoint="category/related", extra_params=category_params
    ).json()
    assert expected == actual


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_category_series(client, return_type):
    actual = client.get_category_series(
        category_id=category_params["category_id"],
        return_format=return_type,
    )
    expected = category_request(
        endpoint="category/series", extra_params=category_params
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "seriess" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        actual_pdf = _convert_to_pandas(expected["seriess"])
        pd.testing.assert_frame_equal(actual_pdf, actual)


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_category_tags(client, return_type):
    actual = client.get_category_tags(
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
def test_get_category_related_tags(client, return_type):
    actual = client.get_category_related_tags(
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
