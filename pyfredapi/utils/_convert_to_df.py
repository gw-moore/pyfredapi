from __future__ import annotations

import pandas as pd

try:
    import polars as pl
    from polars.exceptions import InvalidOperationError

    MISSING_POLARS = False
except ImportError:
    MISSING_POLARS = True


# ! Excluding realtime_start & realtime_end because pandas can't convert the max/min dates in FRED
# ! I'm not sure this is a good idea. Feels hacky, fragile, and I don't like overwriting the source data when converting
# ! But I would like to convert all columns to the correct data type
# ! and pandas does not accept the realtime dates as-is from FRED
# ! A check could be made against the realtime columns, and if the date is out of bounds, the value is overwritten to the min/max that pandas accepts
# ! The overwrite will allow pd.to_datetime to work
# ! The minimum date pandas accepts is 1677-09-21
# ! The maximum date pandas accepts is 2262-04-11
# ! code snippet for converting to valid date:
# for c in date_cols:
#     df.loc[(df[c] < "1677-09-21"), c] = "1677-09-21"
#     df.loc[(df[c] > "2262-04-11"), c] = "2262-04-11"

FRED_DATE_COLS = ["date", "created", "realtime_start", "realtime_end"]
FRED_NUM_COLS = ["value"]


def _convert_to_pandas(data: list[dict]) -> pd.DataFrame:
    """Convert a FRED response dictionary to a pandas dataframe.

    Parameters
    ----------
    data : Dict[str, Any]
        Response from FRED api endpoint.

    Returns
    -------
    Pandas dataframe.

    """
    df = pd.DataFrame(data)
    date_cols = [c for c in list(df.columns) if c in FRED_DATE_COLS]
    for c in date_cols:
        df[c] = pd.to_datetime(df[c], errors="coerce")

    num_cols = [c for c in list(df.columns) if c in FRED_NUM_COLS]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


def _convert_to_polars(data: list[dict]) -> pl.DataFrame:
    """Convert a FRED response dictionary to a pandas dataframe.

    Parameters
    ----------
    data : Dict[str, Any]
        Response from FRED api endpoint.

    Returns
    -------
    Polars DataFrame.

    """
    if MISSING_POLARS:
        raise ImportError(
            "Unable to import polars. Ensure you have the polars package installed."
        )

    df = pl.DataFrame(data)

    date_cols = [c for c in list(df.columns) if c in FRED_DATE_COLS]
    for col in date_cols:
        try:
            df = df.cast({col: pl.Date})
        except InvalidOperationError:
            pass

    num_cols = [c for c in list(df.columns) if c in FRED_NUM_COLS]
    for col in num_cols:
        df = df.filter(pl.col(col) != ".")
        df = df.cast({col: pl.Float64})

    return df
