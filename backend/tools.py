import base64
import io
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from langchain.tools import tool
from typing import Optional

_df: pd.DataFrame = None  # type: ignore
_last_chart_base64: Optional[str] = None


def get_last_chart() -> Optional[str]:
    return _last_chart_base64


def clear_last_chart() -> None:
    global _last_chart_base64
    _last_chart_base64 = None


def set_dataframe(df: pd.DataFrame) -> None:
    global _df
    _df = df


@tool
def query_data(pandas_expression: str) -> str:
    """Execute a pandas expression on the Titanic DataFrame and return the result.

    The DataFrame is available as 'df'. Write valid pandas code to query it.

    PARAMETERS:
        pandas_expression: A valid Python/pandas expression using 'df' as the DataFrame.

    EXAMPLES:
        - "df['sex'].value_counts()" to count males and females
        - "df['age'].mean()" to get the average age
        - "df.groupby('pclass')['survived'].mean() * 100" for survival rate by class
        - "len(df[df['survived'] == 1])" to count survivors
        - "df['fare'].describe()" for fare statistics

    RETURNS:
        The result of the pandas expression as a string, or an error message.
    """
    if _df is None:
        return "Error: Dataset not loaded. Please restart the server."

    try:
        SAFE_BUILTINS = {
            "round": round,
            "len": len,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "sorted": sorted,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "range": range,
            "isinstance": isinstance,
            "True": True,
            "False": False,
            "None": None,
        }

        result = eval(
            pandas_expression,
            {"df": _df, "pd": pd, "np": np, "__builtins__": SAFE_BUILTINS},
        )

        return str(result)

    except Exception as e:
        return f"Error executing query: {str(e)}. Please check the column names and syntax."


@tool
def create_chart(
    chart_type: str,
    column: str,
    title: str,
    hue: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
) -> str:
    """Create a visualization of the Titanic dataset and return it as a base64 PNG.

    PARAMETERS:
        chart_type: Type of chart. One of: 'histogram', 'bar', 'pie', 'box', 'count', 'scatter', 'heatmap'
        column: The main column to visualize (e.g., 'age', 'fare', 'sex', 'pclass')
        title: Title for the chart
        hue: Optional. Column to use for color grouping (e.g., 'survived')
        xlabel: Optional. Custom label for the x-axis
        ylabel: Optional. Custom label for the y-axis

    RETURNS:
        A confirmation message. The chart image is stored internally.
    """
    if _df is None:
        return "Error: Dataset not loaded."

    sns.set_style("whitegrid")
    sns.set_palette("husl")
    fig, ax = plt.subplots(figsize=(10, 6))

    try:
        if chart_type == "histogram":
            sns.histplot(data=_df, x=column, hue=hue, bins=30, kde=True, ax=ax)

        elif chart_type == "bar":
            sns.barplot(data=_df, x=column, hue=hue, y=hue if hue else None, ax=ax)

        elif chart_type == "pie":
            counts = _df[column].value_counts()
            ax.pie(
                counts.values,
                labels=counts.index,
                autopct="%1.1f%%",
                startangle=90,
                colors=sns.color_palette("husl", len(counts)),
            )
            ax.set_aspect("equal")

        elif chart_type == "box":
            if hue:
                sns.boxplot(data=_df, x=hue, y=column, ax=ax)
            else:
                sns.boxplot(data=_df, y=column, ax=ax)

        elif chart_type == "count":
            sns.countplot(data=_df, x=column, hue=hue, ax=ax)
            for patch in ax.patches:
                ax.annotate(
                    f"{int(patch.get_height())}",
                    (patch.get_x() + patch.get_width() / 2.0, patch.get_height()),
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize=11,
                )

        elif chart_type == "scatter":
            scatter_hue = hue if hue and hue != column else None
            sns.scatterplot(
                data=_df,
                x=column,
                y=hue if hue else "fare",
                hue=scatter_hue,
                alpha=0.6,
                ax=ax,
            )

        elif chart_type == "heatmap":
            numeric_df = _df.select_dtypes(include="number")
            correlation = numeric_df.corr()
            sns.heatmap(
                correlation,
                annot=True,
                cmap="coolwarm",
                center=0,
                fmt=".2f",
                ax=ax,
                vmin=-1,
                vmax=1,
            )

        else:
            plt.close(fig)
            return (
                f"Error: Unsupported chart type '{chart_type}'. "
                f"Use one of: histogram, bar, pie, box, count, scatter, heatmap"
            )

        ax.set_title(title, fontsize=14, fontweight="bold")
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=100, bbox_inches="tight", facecolor="white")
        buf.seek(0)
        plt.close(fig)

        image_base64 = base64.b64encode(buf.read()).decode("utf-8")

        global _last_chart_base64
        _last_chart_base64 = image_base64

        return f"Chart '{title}' created successfully."

    except Exception as e:
        plt.close(fig)
        return (
            f"Error creating chart: {str(e)}. Please check column names and chart type."
        )
