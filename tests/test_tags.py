import pytest

from pyfredapi.api.tags import FredTags


@pytest.fixture()
def client():
    return FredTags()


def test_get_tags():
    ...


def test_get_related_tags():
    ...


def test_get_tag_series():
    ...
