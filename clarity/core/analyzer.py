import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union
from pathlib import Path

class DataAnalyzer:
    """Core class for data analysis in Clarity."""
    
    def __init__(self, data: Optional[Union[pd.DataFrame, str, Path]] = None):
        """Initialize the DataAnalyzer with data."""
        self.data = None
        if isinstance(data, (str, Path)):
            self.load_data(data)
        elif isinstance(data, pd.DataFrame):
            self.data = data.copy()
    
    def load_data(self, filepath: Union[str, Path]) -> None:
        """Load data from a file."""
        filepath = Path(filepath)
        if filepath.suffix == '.csv':
            self.data = pd.read_csv(filepath)
        elif filepath.suffix in ['.xls', '.xlsx']:
            self.data = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive summary of the dataset."""
        if self.data is None:
            raise ValueError("No data loaded")
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        categorical_cols = self.data.select_dtypes(exclude=[np.number]).columns
        
        summary = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'numeric_columns': list(numeric_cols),
            'categorical_columns': list(categorical_cols),
            'missing_values': self.data.isnull().sum().to_dict(),
            'duplicates': self.data.duplicated().sum()
        }
        
        # add numeric statistics if there are numeric columns
        if len(numeric_cols) > 0:
            summary['numeric_stats'] = {}
            for col in numeric_cols:
                summary['numeric_stats'][col] = {
                    'mean': self.data[col].mean(),
                    'std': self.data[col].std(),
                    'min': self.data[col].min(),
                    'max': self.data[col].max(),
                    'median': self.data[col].median()
                }
            summary['correlations'] = self.data[numeric_cols].corr().to_dict()
        
        return summary
    
    def analyze_column(self, column: str) -> Dict[str, Any]:
        """Analyze a specific column in detail."""
        if self.data is None:
            raise ValueError("No data loaded")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found")
        
        series = self.data[column]
        analysis = {
            'name': column,
            'dtype': str(series.dtype),
            'unique_count': series.nunique(),
            'missing_count': series.isnull().sum(),
            'missing_percentage': (series.isnull().sum() / len(series)) * 100
        }
        
        if np.issubdtype(series.dtype, np.number):
            analysis.update({
                'mean': series.mean(),
                'median': series.median(),
                'std': series.std(),
                'min': series.min(),
                'max': series.max(),
                'quartiles': series.quantile([0.25, 0.5, 0.75]).to_dict()
            })
        else:
            analysis.update({
                'value_counts': series.value_counts().to_dict(),
                'top_values': series.value_counts().head().to_dict()
            })
        
        return analysis

__all__ = ['DataAnalyzer']
