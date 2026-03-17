# tests/unit/test_polars.py
import polars as pl
import pytest

def test_polars_dataframe():
    df = pl.DataFrame(
        {
            "altitude": [1000.0, 2000.0],
            "airspeed": [150.0, 200.0],
        }
    )
    assert df.shape == (2, 2)
    assert df["altitude"][0] == 1000.0
