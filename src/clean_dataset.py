import pandas as pd

ORIGNAL_PATH: str = "data/original.csv"


def remove_white_spaces(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df[col] = df[col].apply(lambda d: " ".join(d.split()) if isinstance(d, str) else d)
    return df


def split_date_into_seperate_columns(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df.insert(2, f"{col}_year", df[col].dt.year)
    df.insert(3, f"{col}_month", df[col].dt.month)
    df.insert(4, f"{col}_day", df[col].dt.day)
    df.insert(5, f"{col}_hour", df[col].dt.hour)
    df.insert(6, f"{col}_minute", df[col].dt.minute)
    df.insert(7, f"{col}_second", df[col].dt.second)
    df.insert(8, f"{col}_weekday", df[col].dt.weekday)

    return df


def main() -> None:
    df = pd.read_csv(ORIGNAL_PATH)
    df = df.rename(
        columns={
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
    df["vendor_name"] = df["vendor_name"].str.replace("*", "")
    df = remove_white_spaces(df, "vendor_name")
    df = remove_white_spaces(df, "vendor_state_province")
    df = remove_white_spaces(df, "description")

    df["date"] = pd.to_datetime(df["date"])
    df["modify_date"] = pd.to_datetime(df["modify_date"])
    df.insert(2, "seconds_between", (df["modify_date"] - df["date"]).dt.total_seconds())
    df = split_date_into_seperate_columns(df, "modify_date")
    df = split_date_into_seperate_columns(df, "date")

    df = df.sort_values(["agency", "date"])

    df = df.drop(columns=["OBJECTID", "date", "modify_date"])
    df.to_csv("data/clean.csv", index=False)


if __name__ == "__main__":
    main()
