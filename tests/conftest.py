import os
from typing import Dict, Optional

import pytest
import requests

api_key = os.environ.get("FRED_API_KEY")

if api_key is None:
    raise ValueError("Must set FRED_API_KEY in environment before running tests.")

base_params = {
    "api_key": api_key,
    "file_type": "json",
}
BASE_FRED_URL = "https://api.stlouisfed.org/fred"


def base_request(
    endpoint: str,
    extra_params: Optional[Dict[str, str]] = None,
    base_params: Dict[str, str] = base_params,
):
    if extra_params is None:
        extra_params = {}

    return requests.get(
        f"{BASE_FRED_URL}/{endpoint}",
        params={**base_params, **extra_params},
    )


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Exclude the api_key from the url request
        "filter_query_parameters": ["api_key"],
    }
