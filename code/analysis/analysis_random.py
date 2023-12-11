import networkx as nx
import random
import csv
from itertools import combinations, groupby
import matplotlib.pyplot as plt
from matplotlib import cm
import os
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def plot_2d_data():
    filename_1 = "../../data/pa_2_deg/data_all_pa_2_avg.csv"
    filename_2 = "../../data/pa_2_ec/data_all_pa_2_avg.csv"
    filename_3 = "../../data/pa_2_deg_exp/data_all_pa_2_avg.csv"
    filename_4 = "../../data/pa_2_ec_exp/data_all_pa_2_avg.csv"

    # filename_1 = "../../data/random_deg/data_all_random_avg.csv"
    # filename_2 = "../../data/random_ec/data_all_random_avg.csv"
    # filename_3 = "../../data/random_deg_exp/data_all_random_avg.csv"
    # filename_4 = "../../data/random_ec_exp/data_all_random_avg.csv"

    # Read the CSV file into a pandas DataFrame
    df_1 = pd.read_csv(filename_1)
    df_1 = df_1.groupby('size').mean().reset_index()

    df_2 = pd.read_csv(filename_2)
    df_2 = df_2.groupby('size').mean().reset_index()

    df_3 = pd.read_csv(filename_3)
    df_3 = df_3.groupby('size').mean().reset_index()

    df_4 = pd.read_csv(filename_4)
    df_4 = df_4.groupby('size').mean().reset_index()

    # Create a 2D plot
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.plot(df_1['size'], df_1['avg_rate'], marker='o', linestyle='-', label="degree, const")
    plt.plot(df_2['size'], df_2['avg_rate'], marker='o', linestyle='-', label="eigenvector centrality, const")
    plt.plot(df_3['size'], df_3['avg_rate'], marker='o', linestyle='-', label="degree, exp")
    plt.plot(df_4['size'], df_4['avg_rate'], marker='o', linestyle='-', label="eigenvector centrality, exp")

    plt.xlabel('Size')
    plt.ylabel('Average Rate')
    plt.title('Plot of Size vs. Avg Rate, Preferential Attachment Networks')
    # plt.title('Plot of Size vs. Avg Rate, Random Networks')
    plt.legend()

    # Show the plot
    plt.show()

def plot_3d_data():
    filename = "../../data/pa_2_deg/data_all_pa_2_avg.csv"

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)

    # Assuming the first and second columns are named 'Column1' and 'Column2'
    column1 = df['size'].to_numpy()
    column2 = df['n_comp_nodes'].to_numpy()
    # column2 = df['rate'].to_numpy()
    # column3 = df['n_comp_nodes'].to_numpy()
    column3 = df['avg_rate'].to_numpy()

    # Create a 3D plot
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Surface plot
    sc = ax.scatter(column1, column2, column3, c=column3, cmap = 'viridis', alpha = 0.7)
    # surf = ax.plot_trisurf(column1, column2, column3, cmap=cm.viridis, linewidth=.5) # , antialiased=False)

    # Set labels
    ax.set_xlabel('Size')
    ax.set_ylabel('Neighborhood Completion')
    ax.set_zlabel('Average Trial Completion Rate')

    # fig.colorbar(surf, shrink=0.5, aspect=10)
    cbar = plt.colorbar(sc, shrink=0.5, aspect=10)
    # ax.set_title('Completion Rate by Size and Neighborhood Completion, Random')

    # Show the plot
    plt.show()


def main():
    # filename = "../../data/data_summary_random.csv"
    # filename = "../../data/random/data_all_random_avg.csv"
    filename = "../../data/pa_2_deg/data_all_pa_2_avg.csv"
    # filename = "../../data/random/random_5/random_5_0.csv"
    # plot_csv_data(filename)
    plot_2d_data()

    # # Example ranks
    # ranks = np.arange(1, 11)  # Assuming 10 nodes

    # # Calculate weights using np.exp(-rank)
    # weights = 100 * np.exp(-ranks)

    # # Plot the distribution
    # plt.plot(ranks, weights, marker='o')
    # plt.title('Exponential Decay Weight Distribution')
    # plt.xlabel('Rank')
    # plt.ylabel('Weight')
    # plt.show()

if __name__ == "__main__":
    main()