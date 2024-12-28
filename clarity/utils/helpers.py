# Core imports
import pandas as pd
import numpy as np
from typing import Optional, Union, List

def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and perform basic checks on input DataFrame.
    
    Args:
        df: Input DataFrame to validate
        
    Returns:
        Validated DataFrame
        
    Raises:
        ValueError: If input is not a valid DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")
        
    if df.empty:
        raise ValueError("DataFrame is empty")
        
    return df.copy()

def is_numeric_dtype(series: pd.Series) -> bool:
    """Check if a pandas Series has numeric dtype."""
    return pd.api.types.is_numeric_dtype(series)

def is_datetime_dtype(series: pd.Series) -> bool:
    """Check if a pandas Series has datetime dtype."""
    return pd.api.types.is_datetime64_any_dtype(series)

def is_categorical_dtype(series: pd.Series) -> bool:
    """Check if a pandas Series has categorical or object dtype."""
    return pd.api.types.is_categorical_dtype(series) or pd.api.types.is_object_dtype(series)

