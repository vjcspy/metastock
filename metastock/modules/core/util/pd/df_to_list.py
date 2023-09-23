import arrow
import pandas as pd


def df_to_list(df: pd.DataFrame):
    return [
        {**row.to_dict(), 'date': arrow.get(index).format('YYYY-MM-DD')}
        for index, row in df.iterrows()
    ]
