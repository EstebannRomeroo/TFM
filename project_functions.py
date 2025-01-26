import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def categorical_analysis(data, categorical_features):
    """
    This function identifies all categorical variables within a DataFrame
    and calculates the absolute frequency and percentage of each category in those variables.

    Parameters:
    - data (pd.DataFrame): The DataFrame from which to analyze the categorical variables.

    Returns:
    - pd.DataFrame: A DataFrame where each row represents a category of one of
                    the categorical variables, including the absolute frequency and
                    percentage of each category.
    """
    results = {}
    for var in categorical_features:
        values = data[var].value_counts()
        percent = data[var].value_counts(normalize=True) * 100
        results[var] = pd.DataFrame({'values': values, 'percentage': percent})

    results = pd.concat(results)
    return results

def plot_categorical_features(data, categorical_features, graphs_per_fig=9):
    """
    Generates distribution plots for categorical variables, mapping binary values (1, 0) to custom labels if provided.
    Handles missing or unexpected values gracefully.

    Parameters:
    - data: DataFrame containing the data.
    - categorical_features: List of categorical column names or a single column name as a string.
    - graphs_per_fig: Maximum number of plots per figure (default: 9).
    """
    # Ensure categorical_features is a list
    # Check if categorical_features is a single string, and if so, convert it into a list for consistent processing
    if isinstance(categorical_features, str):
        categorical_features = [categorical_features]

    # Calculate the total number of categorical variables
    num_vars = len(categorical_features)

    # Iterate through all categorical variables in chunks defined by graphs_per_fig
    for start in range(0, num_vars, graphs_per_fig):
        # Define the end index for the current batch of features
        end = start + graphs_per_fig

        # Create a new figure with specified size to accommodate up to graphs_per_fig subplots
        plt.figure(figsize=(16, 12))

        # Loop through the current batch of variables and generate individual plots
        for i, var in enumerate(categorical_features[start:end], 1):
            # Add a subplot in a 3x3 grid for the current variable
            plt.subplot(3, 3, i)

            # Generate a countplot for the current categorical variable
            sns.countplot(x=var, data=data, palette='cool')

            # Add a title to the subplot indicating the variable being plotted
            plt.title(f'Distribution of {var}')

            # Rotate x-axis labels slightly for better readability
            plt.xticks(rotation=45)

        # Adjust layout to avoid overlapping plots and ensure proper spacing
        plt.tight_layout()

        # Display the figure containing the plots
        plt.show()

def save_categorical_bar_plots(data, categorical_features):
    """
    Generates bar plots for categorical variables, saves each plot as a PNG file,
    and returns the list of saved file names.

    Args:
        data (pd.DataFrame): The dataset containing the categorical variables.
        categorical_features (list): A list of column names representing categorical features to plot.

    Returns:
        list: A list of file paths for the saved plots.
    """
    # Ensure the 'plots/' directory exists, create it if it doesn't
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # List to store the file paths of saved plots
    saved_files = []

    # Iterate through all categorical variables
    for var in categorical_features:
        # Create a new figure for each variable
        plt.figure(figsize=(8, 6))  # Set the size of the figure

        # Generate a countplot for the current variable
        sns.countplot(
            x=var,  # X-axis: categorical variable
            data=data,  # Dataset containing the variable
            palette='cool'  # Color palette for the plot
        )

        # Set the title for the plot
        plt.title(f'Distribution of {var}')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)

        # Define the file path for saving the plot
        file_path = f'plots/distribution_{var}.png'

        # Save the individual plot as a PNG file in the 'plots/' directory
        plt.savefig(
            file_path,  # Path and file name
            format='png',  # File format
            dpi=300  # Resolution of the plot
        )

        # Close the figure to free up memory and avoid overlapping plots
        plt.close()

        # Append the file path to the list of saved files
        saved_files.append(file_path)

    # Return the list of saved file paths
    return saved_files

def remove_outliers(data, numeric_features, factor=1.5):
    """
    Removes outliers from a dataset based on the Interquartile Range (IQR) method.

    Parameters:
        data (pd.DataFrame): The input DataFrame containing the data.
        numeric_features (list): List of column names corresponding to numeric features to process.
        factor (float): The multiplier for the IQR to define outlier thresholds (default is 1.5).

    Returns:
        pd.DataFrame: A DataFrame with outliers removed from the specified numeric features.
    """
    feature_data = data[numeric_features].copy()
    for col in feature_data.columns:
        q1 = feature_data[col].quantile(0.25)
        q3 = feature_data[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - factor * iqr
        upper_bound = q3 + factor * iqr

        # Filter values within the bounds
        filtered_data = feature_data[(feature_data[col] >= lower_bound) & (feature_data[col] <= upper_bound)]
    return filtered_data

def missing_values_analysis(data):
    """
    Analyzes missing values in the dataset, calculates their count and percentage,
    and generates a summary DataFrame of columns with missing values.

    Parameters:
    - data: pandas.DataFrame
        The dataset to analyze.

    Returns:
    - pandas.DataFrame
        A DataFrame containing:
        - 'Missing Values': The total number of missing values for each column.
        - 'Percentage (%)': The percentage of missing values relative to the total number of rows.
        - Only columns with missing values are included, sorted by percentage in descending order.

    Example Usage:
    ```
    missing_summary = missing_values_analysis(data)
    print(missing_summary)
    ```

    Steps:
    1. Calculate the total number of rows in the dataset (`total_rows`).
    2. Compute the total count of missing values for each column (`missing_data`).
    3. Calculate the percentage of missing values for each column relative to the dataset size (`missing_percentage`).
    4. Combine the count and percentage into a summary DataFrame (`missing_summary`).
    5. Filter out columns with no missing values and sort by percentage in descending order.
    """
    # Total number of rows in the dataset
    total_rows = len(data)

    # Identify columns with missing values and calculate the count and percentage
    missing_data = data.isnull().sum()  # Total missing values per column
    missing_percentage = (missing_data / total_rows) * 100  # Calculate percentage

    # Combine counts and percentages into a DataFrame
    missing_summary = pd.DataFrame({
        'Missing Values': missing_data,
        'Percentage (%)': missing_percentage
    })

    # Filter only columns with missing values
    missing_summary = missing_summary[missing_summary['Missing Values'] > 0]

    # Sort columns by percentage of missing values in descending order
    missing_summary = missing_summary.sort_values(by='Percentage (%)', ascending=False)

    # Display the top rows of the summary
    return missing_summary








