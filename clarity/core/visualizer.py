import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Union, List, Optional, Tuple, Dict
from pathlib import Path

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

class DataVisualizer:
    """Core class for data visualization in Clarity."""
    
    def __init__(self, data: Optional[Union[pd.DataFrame, str, Path]] = None):
        """Initialize the DataVisualizer with data."""
        self.data = None
        if isinstance(data, (str, Path)):
            self.load_data(data)
        elif isinstance(data, pd.DataFrame):
            self.data = data.copy()
        
        # Set default style based on available packages
        try:
            if HAS_SEABORN:
                plt.style.use('seaborn')
            else:
                plt.style.use('default')
        except:
            plt.style.use('default')
    
    def load_data(self, filepath: Union[str, Path]) -> None:
        """Load data from a file."""
        filepath = Path(filepath)
        if filepath.suffix == '.csv':
            self.data = pd.read_csv(filepath)
        elif filepath.suffix in ['.xls', '.xlsx']:
            self.data = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
    
    def plot_distribution(self, 
                         column: str,
                         plot_type: str = 'auto',
                         figsize: Tuple[int, int] = (10, 6)) -> None:
        """Plot the distribution of a column.
        
        Args:
            column: Name of the column to plot
            plot_type: 'hist', 'box', 'violin', or 'auto'
            figsize: Figure size as (width, height)
        """
        if self.data is None:
            raise ValueError("No data loaded")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found")
        
        plt.figure(figsize=figsize)
        
        if plot_type == 'auto':
            if np.issubdtype(self.data[column].dtype, np.number):
                if HAS_SEABORN:
                    sns.histplot(data=self.data, x=column, kde=True)
                else:
                    plt.hist(self.data[column].dropna(), bins=30, edgecolor='black')
            else:
                self.data[column].value_counts().plot(kind='bar')
        elif plot_type == 'hist':
            if HAS_SEABORN:
                sns.histplot(data=self.data, x=column, kde=True)
            else:
                plt.hist(self.data[column].dropna(), bins=30, edgecolor='black')
        elif plot_type == 'box':
            if HAS_SEABORN:
                sns.boxplot(data=self.data, y=column)
            else:
                plt.boxplot(self.data[column].dropna())
        elif plot_type == 'violin':
            if HAS_SEABORN:
                sns.violinplot(data=self.data, y=column)
            else:
                plt.boxplot(self.data[column].dropna())  # Fallback to boxplot if no seaborn
        else:
            raise ValueError("Invalid plot type")
        
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.tight_layout()
        plt.show()

    def plot_correlation_matrix(self, 
                              columns: Optional[List[str]] = None,
                              figsize: Tuple[int, int] = (10, 8)) -> None:
        """Plot correlation matrix for numeric columns.
        
        Args:
            columns: List of columns to include, or None for all numeric columns
            figsize: Figure size as (width, height)
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        # Select numeric columns
        if columns is None:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        else:
            numeric_cols = [col for col in columns if np.issubdtype(self.data[col].dtype, np.number)]
            
        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns available")
            
        # Calculate correlation matrix
        corr_matrix = self.data[numeric_cols].corr()
        
        # Create heatmap
        plt.figure(figsize=figsize)
        sns.heatmap(corr_matrix, 
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   vmin=-1, 
                   vmax=1)
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.show()

    def plot_scatter(self,
                    x: str,
                    y: str,
                    hue: Optional[str] = None,
                    figsize: Tuple[int, int] = (10, 6)) -> None:
        """Create a scatter plot of two numeric columns.
        
        Args:
            x: Column name for x-axis
            y: Column name for y-axis
            hue: Column name for color coding points
            figsize: Figure size as (width, height)
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        plt.figure(figsize=figsize)
        sns.scatterplot(data=self.data, x=x, y=y, hue=hue)
        plt.title(f'{y} vs {x}')
        plt.tight_layout()
        plt.show()

    def plot_time_series(self,
                        date_column: str,
                        value_column: str,
                        figsize: Tuple[int, int] = (12, 6)) -> None:
        """Plot a time series.
        
        Args:
            date_column: Name of the column containing dates
            value_column: Name of the column containing values to plot
            figsize: Figure size as (width, height)
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        # Ensure date column is datetime
        try:
            self.data[date_column] = pd.to_datetime(self.data[date_column])
        except:
            raise ValueError(f"Could not convert {date_column} to datetime")
            
        plt.figure(figsize=figsize)
        plt.plot(self.data[date_column], self.data[value_column])
        plt.title(f'Time Series of {value_column}')
        plt.xlabel(date_column)
        plt.ylabel(value_column)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_missing_values(self, figsize: Tuple[int, int] = (10, 6)) -> None:
        """Plot missing values heatmap."""
        if self.data is None:
            raise ValueError("No data loaded")
            
        plt.figure(figsize=figsize)
        sns.heatmap(self.data.isnull(), 
                   yticklabels=False,
                   cmap='viridis',
                   cbar_kws={'label': 'Missing Values'})
        plt.title('Missing Values Heatmap')
        plt.tight_layout()
        plt.show()

    def save_plot(self, filename: Union[str, Path]) -> None:
        """Save the current plot to a file."""
        plt.savefig(filename)

    def create_dashboard(self, 
                        numeric_columns: Optional[List[str]] = None,
                        figsize: Tuple[int, int] = (15, 10)) -> None:
        """Create a basic dashboard of visualizations.
        
        Args:
            numeric_columns: List of numeric columns to include
            figsize: Figure size as (width, height)
        """
        if self.data is None:
            raise ValueError("No data loaded")
            
        if numeric_columns is None:
            numeric_columns = list(self.data.select_dtypes(include=[np.number]).columns)
            
        # Create subplot grid
        n_cols = min(len(numeric_columns), 3)
        n_rows = (len(numeric_columns) + 2) // 3  # +2 for correlation matrix and missing values
        
        fig = plt.figure(figsize=figsize)
        
        # Plot distributions
        for i, col in enumerate(numeric_columns, 1):
            plt.subplot(n_rows, n_cols, i)
            sns.histplot(data=self.data, x=col, kde=True)
            plt.title(f'Distribution of {col}')
            
        plt.tight_layout()
        plt.show()

