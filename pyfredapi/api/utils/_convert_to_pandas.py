from typing import Any, Dict

import pandas as pd

# excluding realtime_start & realtime_end because pandas can't convert
# the max/min dates available in FRED
FRED_DATE_COLS = [
    # "realtime_start",
    # "realtime_end",
    "date",
]

FRED_NUM_COLS = ["value"]


def _convert_to_pandas(data: Dict[str, Any]) -> pd.DataFrame:
    """Convert a FRED response dictionary to a pandas dataframe.

    Parameters
    ----------
    response : Dict[str, Any]
        Response from FRED api endpoint.
    key : str
        Key for data in response dictionary.

    Returns
    -------
    Pandas dataframe
    """
    df = pd.DataFrame.from_dict(data)

    date_cols = [c for c in list(df.columns) if c in FRED_DATE_COLS]
    for c in date_cols:
        df[c] = pd.to_datetime(df[c])

    num_cols = [c for c in list(df.columns) if c in FRED_NUM_COLS]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df
