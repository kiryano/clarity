import pandas as pd
import numpy as np
from typing import Union, List, Optional, Dict, Any
from pathlib import Path

class DataCleaner:
    """Core class for data cleaning in Clarity."""
    
    def __init__(self, data: Optional[Union[pd.DataFrame, str, Path]] = None):
        """Initialize the DataCleaner with data."""
        self.data = None
        self.original_data = None
        if isinstance(data, (str, Path)):
            self.load_data(data)
        elif isinstance(data, pd.DataFrame):
            self.data = data.copy()
            self.original_data = data.copy()
    
    def load_data(self, filepath: Union[str, Path]) -> None:
        """Load data from a file."""
        filepath = Path(filepath)
        if filepath.suffix == '.csv':
            self.data = pd.read_csv(filepath)
        elif filepath.suffix in ['.xls', '.xlsx']:
            self.data = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
        self.original_data = self.data.copy()
    
    def remove_duplicates(self, subset: Optional[List[str]] = None) -> None:
        """Remove duplicate rows."""
        if self.data is None:
            raise ValueError("No data loaded")
        self.data = self.data.drop_duplicates(subset=subset)
    
    def handle_missing_values(self, 
                            strategy: str = 'mean',
                            columns: Optional[List[str]] = None,
                            fill_value: Any = None) -> None:
        """Handle missing values in the dataset.
        
        Args:
            strategy: One of 'mean', 'median', 'mode', 'drop', or 'fill'
            columns: Specific columns to handle, or None for all
            fill_value: Value to use if strategy is 'fill'
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        if columns is None:
            columns = self.data.columns
        
        for column in columns:
            if column not in self.data.columns:
                continue
                
            if strategy == 'drop':
                self.data = self.data.dropna(subset=[column])
            elif strategy == 'fill' and fill_value is not None:
                self.data[column] = self.data[column].fillna(fill_value)
            else:
                if np.issubdtype(self.data[column].dtype, np.number):
                    if strategy == 'mean':
                        value = self.data[column].mean()
                    elif strategy == 'median':
                        value = self.data[column].median()
                    else:
                        value = self.data[column].mode()[0] if not self.data[column].mode().empty else None
                else:
                    value = self.data[column].mode()[0] if not self.data[column].mode().empty else None
                
                if value is not None:
                    self.data[column] = self.data[column].fillna(value)
    
    def normalize_column(self, column: str, method: str = 'minmax') -> None:
        """Normalize values in a numeric column.
        
        Args:
            column: Name of the column to normalize
            method: One of 'minmax', 'zscore'
        """
        if self.data is None:
            raise ValueError("No data loaded")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found")
        if not np.issubdtype(self.data[column].dtype, np.number):
            raise ValueError(f"Column '{column}' is not numeric")
        
        if method == 'minmax':
            min_val = self.data[column].min()
            max_val = self.data[column].max()
            self.data[column] = (self.data[column] - min_val) / (max_val - min_val)
        elif method == 'zscore':
            mean = self.data[column].mean()
            std = self.data[column].std()
            self.data[column] = (self.data[column] - mean) / std
        else:
            raise ValueError("Method must be 'minmax' or 'zscore'")
    
    def remove_outliers(self, column: str, method: str = 'iqr') -> None:
        """Remove outliers from a numeric column.
        
        Args:
            column: Name of the column
            method: One of 'iqr' or 'zscore'
        """
        if self.data is None:
            raise ValueError("No data loaded")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found")
        if not np.issubdtype(self.data[column].dtype, np.number):
            raise ValueError(f"Column '{column}' is not numeric")
        
        if method == 'iqr':
            Q1 = self.data[column].quantile(0.25)
            Q3 = self.data[column].quantile(0.75)
            IQR = Q3 - Q1
            mask = ~((self.data[column] < (Q1 - 1.5 * IQR)) | (self.data[column] > (Q3 + 1.5 * IQR)))
        elif method == 'zscore':
            zscore = np.abs((self.data[column] - self.data[column].mean()) / self.data[column].std())
            mask = zscore <= 3
        else:
            raise ValueError("Method must be 'iqr' or 'zscore'")
        
        self.data = self.data[mask]
    
    def reset_to_original(self) -> None:
        """Reset the data to its original state."""
        if self.original_data is not None:
            self.data = self.original_data.copy()
            
    def get_cleaning_summary(self) -> Dict[str, Any]:
        """Get a summary of the cleaning operations' effects."""
        if self.data is None or self.original_data is None:
            raise ValueError("No data loaded")
            
        return {
            'original_shape': self.original_data.shape,
            'current_shape': self.data.shape,
            'rows_removed': len(self.original_data) - len(self.data),
            'missing_values_original': self.original_data.isnull().sum().to_dict(),
            'missing_values_current': self.data.isnull().sum().to_dict(),
        }
