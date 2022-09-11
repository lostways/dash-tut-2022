from typing import Callable
from functools import reduce, partial
import pandas as pd
import datetime as dt
import babel.dates
import i18n


class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


# Define preporcessor type
Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def process_years(data: pd.DataFrame) -> pd.DataFrame:
    data[DataSchema.YEAR] = data[DataSchema.DATE].dt.year.astype(str)
    return data


def translate_date(data: pd.DataFrame, locale: str) -> pd.DataFrame:
    def date_repr(date: dt.date) -> str:
        return babel.dates.format_date(date, format="MMMM", locale=locale)

    data[DataSchema.MONTH] = data[DataSchema.DATE].apply(date_repr)
    return data


def translate_category(data: pd.DataFrame) -> pd.DataFrame:
    def category_repr(category: str) -> str:
        return i18n.t(f"category.{category}")

    data[DataSchema.CATEGORY] = data[DataSchema.CATEGORY].apply(category_repr)
    return data


def load_transaction_data(path: str, locale: str) -> pd.DataFrame:
    # load data from CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.CATEGORY: str,
        },
        parse_dates=[DataSchema.DATE],
    )

    process: Preprocessor = compose(
        process_years, translate_category, partial(translate_date, locale=locale)
    )
    return process(data)
