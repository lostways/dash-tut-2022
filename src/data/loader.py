import pandas as pd


class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def load_transaction_data(path: str) -> pd.DataFrame:
    # load data from CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.CATEGORY: str,
        },
        parse_dates=[DataSchema.DATE],
    )

    data[DataSchema.MONTH] = data[DataSchema.DATE].dt.month.astype(str)
    data[DataSchema.YEAR] = data[DataSchema.DATE].dt.year.astype(str)

    return data
