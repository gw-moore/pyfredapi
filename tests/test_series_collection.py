import pandas as pd
import pytest

from pyfredapi.series_collection import SeriesCollection, SeriesData


def test_init():
    sc = SeriesCollection()
    assert isinstance(sc, SeriesCollection)


@pytest.mark.vcr()
def test_add_series():
    sc = SeriesCollection()
    sc.add_series("CPIAUCSL")
    assert hasattr(sc, "CPIAUCSL")
    assert isinstance(sc.CPIAUCSL, SeriesData)
    assert isinstance(sc.data["CPIAUCSL"], SeriesData)


def test_drop_series():
    sc = SeriesCollection()
    sc.CPIAUCSL = None
    sc.data = {"CPIAUCSL": None}
    assert hasattr(sc, "CPIAUCSL")
    sc.drop_series("CPIAUCSL")
    assert not hasattr(sc, "CPIAUCSL")


def test_drop_series_err():
    with pytest.raises(ValueError):
        sc = SeriesCollection()
        sc.drop_series("foobar")


@pytest.mark.vcr()
def test_keep_realtime_cols():
    sc = SeriesCollection()
    sc.add_series("CPIAUCSL", drop_realtime=False)
    df_cols = set(sc.CPIAUCSL.df.columns.to_list())
    assert set(("date", "CPIAUCSL", "realtime_start", "realtime_end")) == df_cols


def parse_cpi_title(title: str) -> str:
    """Parse CPI series title into a readable label."""
    return (
        title.lower()
        .replace("consumer price index", "cpi ")
        .replace(" for all urban consumers: ", "")
        .replace(" in u.s. city average", "")
        .replace(" ", "_")
        # .capitalize()
    )


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "rename", [{"CPIAUCSL": "cpi_all_items"}, parse_cpi_title], ids=["dict", "func"]
)
def test_rename_on_add(rename):
    sc = SeriesCollection()
    sc.add_series("CPIAUCSL", rename=rename)
    df_cols = set(sc.CPIAUCSL.df.columns.to_list())
    assert set(("date", "cpi_all_items")) == df_cols


@pytest.mark.vcr()
def test_rename_err():
    with pytest.raises(TypeError):
        sc = SeriesCollection()
        sc.add_series("CPIAUCSL", rename="foobar")


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "rename", [{"CPIAUCSL": "cpi_all_items"}, parse_cpi_title], ids=["dict", "func"]
)
def test_rename_after_add(rename):
    sc = SeriesCollection()
    sc.add_series("CPIAUCSL")
    sc.rename_series(rename=rename)
    df_cols = set(sc.CPIAUCSL.df.columns.to_list())
    assert set(("date", "cpi_all_items")) == df_cols


@pytest.mark.vcr()
def test_rename_partial():
    rename = {"CPIAUCSL": "cpi_all_items"}
    sc = SeriesCollection()
    sc.add_series(["CPIAUCSL", "CPILFESL"])
    sc.rename_series(rename=rename)
    assert set(("date", "cpi_all_items")) == set(sc.CPIAUCSL.df.columns.to_list())
    assert set(("date", "CPILFESL")) == set(sc.CPILFESL.df.columns.to_list())


@pytest.mark.vcr()
def test_merge_long():
    series = ["CPIAUCSL", "CPILFESL"]
    sc = SeriesCollection()
    sc.add_series(series)
    long_df = sc.merge_long()
    assert isinstance(long_df, pd.DataFrame)
    cols = set(long_df.columns.to_list())
    assert set(("date", "value", "series")) == cols
    assert set(series) == set(long_df.series.tolist())


@pytest.mark.vcr()
def test_merge_asof():
    series = ["CPIAUCSL", "CPILFESL"]
    sc = SeriesCollection()
    sc.add_series(series)
    asof_df = sc.merge_asof(base_series_id="CPIAUCSL")
    assert isinstance(asof_df, pd.DataFrame)
    cols = set(asof_df.columns.to_list())
    assert set(["date"] + series) == cols
    assert set(series) == set([c for c in asof_df.columns.tolist() if c != "date"])


@pytest.mark.vcr()
def test_merge_wide():
    series = ["CPIAUCSL", "CPILFESL"]
    sc = SeriesCollection()
    sc.add_series(series)
    wide_df = sc.merge_wide()
    assert isinstance(wide_df, pd.DataFrame)
    cols = set(wide_df.columns.to_list())
    assert set(["date"] + series) == cols
    assert set(series) == set([c for c in wide_df.columns.tolist() if c != "date"])


@pytest.mark.vcr()
def test_list_methods_same():
    sc = SeriesCollection()
    sc.add_series("CPIAUCSL")
    sc.list_series()
    sc.list_end_date()
    sc.list_frequency()
    sc.list_seasonality()
    sc.list_start_date()
    sc.list_units()


@pytest.mark.vcr()
def test_list_methods_diff():
    sc = SeriesCollection()
    sc.add_series(["CPIAUCSL", "WGS10YR"])
    sc.list_series()
    sc.list_end_date()
    sc.list_frequency()
    sc.list_seasonality()
    sc.list_start_date()
    sc.list_units()


def test_plot():
    with pytest.raises(NotImplementedError):
        sc = SeriesCollection()
        sc.plot()


def test_extract_series():
    with pytest.raises(NotImplementedError):
        sc = SeriesCollection()
        sc.extract_series()
