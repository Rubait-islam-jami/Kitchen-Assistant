import pandas as pd
import minsearch
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "recipes_documents.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["id"] = range(len(df))
    return df


def build_index(df):

    index = minsearch.Index(
        text_fields=["document"],
        keyword_fields=["name"]
    )

    index.fit(df.to_dict(orient="records"))

    return index


def ingest():

    df = load_data()

    index = build_index(df)

    return df, index


if __name__ == "__main__":

    df, index = ingest()

    print(f"Loaded {len(df)} recipes.")
    print("Index created successfully.")