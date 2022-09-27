import os
from typing import Dict, Optional

import pandas as pd
import pytest
import requests

from pyfredapi import FredCategory
from pyfredapi.api.utils import _convert_to_pandas

from .conftest import BASE_FRED_URL

base_params = {
    "api_key": os.environ.get("FRED_API_KEY", None),
    "file_type": "json",
    "category_id": 125,
}


@pytest.fixture()
def client():
    return FredCategory()


@pytest.mark.vcr()
def category_request(endpoint: str, extra_params: Optional[Dict[str, str]] = None):
    if extra_params is None:
        extra_params = {}

    return requests.get(
        f"{BASE_FRED_URL}/{endpoint}",
        params={**base_params, **extra_params},
    )


@pytest.mark.vcr()
def test_get_category(client):
    actual = client.get_category(base_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)
    assert category_request("category").json() == actual


@pytest.mark.vcr()
def test_get_category_children(client):
    actual = client.get_category_children(base_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)
    assert category_request("category/children").json() == actual


@pytest.mark.vcr()
def test_get_category_related(client):
    actual = client.get_category_related(base_params["category_id"])
    assert actual is not None
    assert isinstance(actual, dict)
    assert isinstance(actual["categories"], list)
    assert category_request("category/related").json() == actual


@pytest.mark.vcr()
@pytest.mark.parametrize("return_type", ["json", "pandas"])
def test_get_category_series(client, return_type):
    actual = client.get_category_series(
        category_id=base_params["category_id"],
        return_format=return_type,
    )
    expected = category_request("category/series").json()

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
        category_id=base_params["category_id"],
        return_format=return_type,
    )
    expected = category_request("category/tags").json()

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
        category_id=base_params["category_id"],
        return_format=return_type,
        **{"tag_names": "balance"},
    )

    expected = category_request(
        "category/related_tags", extra_params={"tag_names": "balance"}
    ).json()

    if return_type == "json":
        assert isinstance(actual, dict)
        assert "tags" in actual
        assert expected == actual
    elif return_type == "pandas":
        assert isinstance(actual, pd.DataFrame)
        pd.testing.assert_frame_equal(pd.DataFrame.from_dict(expected["tags"]), actual)
