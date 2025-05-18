import polars as pl

ORIGNAL_PATH: str = "data/original.csv"


def remove_white_spaces(df: pl.DataFrame, col: str) -> pl.DataFrame:
    df = df.with_columns((pl.col(col).str.replace_all(r"\s+", " ")))
    return df


def split_date_into_seperate_columns(df: pl.DataFrame, col: str) -> pl.DataFrame:
    df = df.with_columns(
        [
            (pl.col(col).dt.year()).alias(f"{col[0]}_year"),
            (pl.col(col).dt.month()).alias(f"{col[0]}_month"),
            (pl.col(col).dt.day()).alias(f"{col[0]}_day"),
            (pl.col(col).dt.hour()).alias(f"{col[0]}_hour"),
            (pl.col(col).dt.minute()).alias(f"{col[0]}_minute"),
            (pl.col(col).dt.second()).alias(f"{col[0]}_second"),
            (pl.col(col).dt.weekday()).alias(f"{col[0]}_weekday"),
        ]
    )

    return df


def main() -> None:
    df = pl.read_csv(ORIGNAL_PATH)
    df = df.rename(
        {
            "AGENCY": "agency",
            "TRANSACTION_DATE": "date",
            "TRANSACTION_AMOUNT": "amount",
            "VENDOR_NAME": "vendor_name",
            "VENDOR_STATE_PROVINCE": "vendor_state_province",
            "MCC_DESCRIPTION": "description",
            "DCS_LAST_MOD_DTTM": "modify_date",
        }
    )

    df = remove_white_spaces(df, "agency")
    df = remove_white_spaces(df, "vendor_name")
    df = remove_white_spaces(df, "vendor_state_province")
    df = remove_white_spaces(df, "description")
    df = df.with_columns((pl.col("vendor_name").str.replace_all(r"\*", "")))

    df = df.with_columns(
        [
            pl.col("modify_date").str.strptime(pl.Datetime, "%Y/%m/%d %H:%M:%S+00"),
            pl.col("date").str.strptime(pl.Datetime, "%Y/%m/%d %H:%M:%S+00"),
        ]
    )
    df = df.with_columns(
        (pl.col("modify_date") - pl.col("date")).dt.total_seconds().alias("seconds")
    )
    df = split_date_into_seperate_columns(df, "modify_date")
    df = split_date_into_seperate_columns(df, "date")

    df = df.sort(["agency", "date"])

    df = df.drop(["OBJECTID"])
    df = df.select(
        [
            "agency",
            "d_year",
            "d_month",
            "d_day",
            "d_hour",
            "d_minute",
            "d_second",
            "d_weekday",
            "m_year",
            "m_month",
            "m_day",
            "m_hour",
            "m_minute",
            "m_second",
            "m_weekday",
            "seconds",
            "amount",
            "vendor_name",
            "vendor_state_province",
            "description",
        ]
    )
    df.write_csv("data/clean.csv")


if __name__ == "__main__":
    main()
