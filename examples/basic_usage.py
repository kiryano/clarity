import pandas as pd
import numpy as np
# Import directly from clarity package
from clarity.core.analyzer import DataAnalyzer
from clarity.core.cleaner import DataCleaner
from clarity.core.visualizer import DataVisualizer

def create_sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'age': np.random.normal(35, 10, 1000),
        'income': np.random.lognormal(10, 0.5, 1000),
        'satisfaction': np.random.randint(1, 6, 1000),
        'city': np.random.choice(['New York', 'London', 'Tokyo', 'Paris'], 1000),
        'subscription': np.random.choice(['Free', 'Premium', 'Pro'], 1000)
    })

def main():
    # Create sample data
    print("Creating sample data...")
    data = create_sample_data()

    # Add some missing values and outliers
    data.loc[np.random.choice(data.index, 50), 'income'] = np.nan
    data.loc[np.random.choice(data.index, 20), 'age'] = np.random.normal(100, 5, 20)

    print("\nTesting DataAnalyzer...")
    analyzer = DataAnalyzer(data)

    # Get summary statistics
    summary = analyzer.get_summary()
    print("\nData Summary:")
    print(f"Shape: {summary['shape']}")
    print(f"Columns: {summary['columns']}")
    print("\nMissing Values:")
    print(summary['missing_values'])

    # Analyze specific column
    age_analysis = analyzer.analyze_column('age')
    print("\nAge Column Analysis:")
    print(f"Mean: {age_analysis['mean']:.2f}")
    print(f"Median: {age_analysis['median']:.2f}")
    print(f"Std Dev: {age_analysis['std']:.2f}")

    print("\nTesting DataCleaner...")
    cleaner = DataCleaner(data)

    # Clean the data
    print("\nCleaning Data...")
    cleaner.handle_missing_values(strategy='mean', columns=['income'])
    cleaner.remove_outliers('age', method='iqr')

    # Get cleaning summary
    cleaning_summary = cleaner.get_cleaning_summary()
    print("\nCleaning Summary:")
    print(f"Original Shape: {cleaning_summary['original_shape']}")
    print(f"Current Shape: {cleaning_summary['current_shape']}")
    print(f"Rows Removed: {cleaning_summary['rows_removed']}")

    print("\nTesting DataVisualizer...")
    visualizer = DataVisualizer(cleaner.data)

    print("\nGenerating plots...")
    visualizer.plot_distribution('age', plot_type='hist')
    visualizer.plot_distribution('satisfaction', plot_type='box')
    visualizer.plot_correlation_matrix()
    visualizer.plot_missing_values()

if __name__ == "__main__":
    main()

