import os
import time
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


def pytest_addoption(parser):
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="Slow down tests to not overload the FRED API. (Y/N)",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


@pytest.fixture(scope="session")
def runslow(request):
    return request.config.getoption("--runslow")


@pytest.fixture(autouse=True)
def slow_down_tests(runslow):
    yield

    if runslow:
        time.sleep(0.5)


def get_request(
    endpoint: str,
    extra_params: Optional[Dict[str, str]] = None,
    base_params: Dict[str, str] = base_params,
):
    if extra_params is None:
        extra_params = {}

    return requests.get(
        f"{BASE_FRED_URL}/{endpoint}",
        params={**base_params, **extra_params},
        timeout=30,
    )


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Exclude the api_key from the url request
        "filter_query_parameters": ["api_key"],
    }


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    # Put all cassettes in vhs/{module}/{test}.yaml
    return os.path.join("tests/vhs", request.module.__name__.split(".")[-1])
