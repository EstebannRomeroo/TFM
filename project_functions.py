import matplotlib.pyplot as plt
import seaborn as sns
import os


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