import matplotlib.pyplot as plt
import numpy as np

def plot_explained_variance(n_components_values, explained_variances):
    plt.plot(n_components_values, explained_variances, marker='o')
    plt.xlabel('Number of Components (n_components)')
    plt.ylabel('Explained Variance')
    plt.title('Explained Variance vs. Number of Components')
    plt.grid(True)
    plt.show()

def plot_dbscan_clusters(reduced_data, labels, labelIDs):
    for label in labelIDs:
        if label == -1:
            plt.scatter(reduced_data[labels == label, 0], reduced_data[labels == label, 1], color='black', label='Outliers')
        else:
            plt.scatter(reduced_data[labels == label, 0], reduced_data[labels == label, 1], label=f'Face {label}')
    
    plt.legend()
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('DBSCAN Clustering with PCA')
    plt.show()

def save_plots():
    # Example of saving a plot
    plot_files = []

    # Plot example 1
    plt.figure()
    # Your plotting code here...
    plt.savefig('plot1.png')
    plot_files.append('plot1.png')

    # Plot example 2
    plt.figure()
    # Your plotting code here...
    plt.savefig('plot2.png')
    plot_files.append('plot2.png')

    return plot_files
    