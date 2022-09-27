import os

import pytest

base_params = {
    "api_key": os.environ.get("FRED_API_KEY", None),
    "file_type": "json",
}
BASE_FRED_URL = "https://api.stlouisfed.org/fred"


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Exclude the api_key from the url request
        "filter_query_parameters": ["api_key"],
    }
