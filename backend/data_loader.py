import pandas as pd
import seaborn as sns
from backend.config import DATA_PATH


def load_titanic_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
    else:
        df = sns.load_dataset("titanic")

    df["age"] = df["age"].fillna(df["age"].median())
    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])
    df["embark_town"] = df["embark_town"].fillna(df["embark_town"].mode()[0])
    df["fare"] = df["fare"].fillna(df["fare"].median())

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    return df


def get_dataset_summary(df: pd.DataFrame) -> str:
    summary = f"Dataset has {len(df)} rows and {len(df.columns)} columns.\n\n"
    summary += "Columns and their details:\n"

    for col in df.columns:
        dtype = df[col].dtype
        n_unique = df[col].nunique()
        n_missing = df[col].isnull().sum()

        if n_unique <= 10:
            values = df[col].unique().tolist()
            summary += (
                f"  - {col} ({dtype}): {n_unique} unique values: {values}, "
                f"{n_missing} missing\n"
            )
        else:
            summary += (
                f"  - {col} ({dtype}): {n_unique} unique values, "
                f"range: {df[col].min()} to {df[col].max()}, "
                f"{n_missing} missing\n"
            )

    return summary
