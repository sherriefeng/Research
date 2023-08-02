import networkx as nx
import random
import csv
from itertools import combinations, groupby
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def plot_mod_3v(csv_file):
    df = pd.read_csv(csv_file)

    # plt.scatter(df['k'], df['size'], c=df['ave_steps'], cmap='viridis', alpha=0.7)
    # plt.xlabel('k')
    # plt.ylabel('size')
    # plt.colorbar(label='steps')
    # plt.title('DoL Simulations Colored by # Steps')
    # plt.show()

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(df['size'], df['k'], df['ave_steps'])
    # ax.set_xlabel('Size')
    # ax.set_ylabel('# Of Connections Per Node')
    # ax.set_zlabel('Avg # Of Steps')
    # plt.title('DoL Simulation Trials, # Steps')
    # plt.show()

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.scatter(df['size'], df['ave_steps'])
    plt.xlabel('Size')
    plt.ylabel('Avg # Of Steps')
    plt.title('Size vs. Steps')

    plt.subplot(1, 3, 2)
    plt.scatter(df['k'], df['ave_steps'])
    plt.xlabel('# Of Connections Per Node')
    plt.ylabel('Avg # Of Steps')
    plt.title('K vs. Steps')

    plt.subplot(1, 3, 3)
    plt.scatter(df['ave_density'], df['ave_steps'])
    plt.xlabel('Avg Density')
    plt.ylabel('Avg # Of Steps')
    plt.title('Density vs. Steps')

    plt.tight_layout()
    plt.show()

def plot_mod_4v(csv_file):
    df = pd.read_csv(csv_file)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the data points in 3D space, using 'k', 'n', and 'd' as the x, y, and z coordinates, respectively
    # Use color or marker style to represent the 'r' variable
    scatter = ax.scatter(df['k'], df['size'], df['ave_density'], c=df['ave_steps'], cmap='viridis', alpha=0.7)

    # Add labels for each axis
    ax.set_xlabel('# of Connections Per Node')
    ax.set_ylabel('Size')
    ax.set_zlabel('Density')

    # Add a colorbar to represent the 'r' variable
    # cbar = plt.colorbar(scatter, label='Avg Num of Incomplete Nodes')
    # plt.title('DoL Simulations Colored by # of Incomplete Nodes')

    cbar = plt.colorbar(scatter, label='Avg Num of Steps')
    plt.title('DoL Simulations Colored by # of Steps')

    # Show the plot
    plt.show()

def plot_incomp_4v(csv_file):
    df = pd.read_csv(csv_file)
    df['incomp_nodes'] = (1 - df['ave_rate']) * df['size']

    # print(df)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the data points in 3D space, using 'k', 'n', and 'd' as the x, y, and z coordinates, respectively
    # Use color or marker style to represent the 'r' variable
    scatter = ax.scatter(df['k'], df['size'], df['ave_density'], c=df['incomp_nodes'], cmap='viridis', alpha=0.7)

    # Add labels for each axis
    ax.set_xlabel('# of Connections Per Node')
    ax.set_ylabel('Size')
    ax.set_zlabel('Density')

    # Add a colorbar to represent the 'r' variable
    cbar = plt.colorbar(scatter, label='Avg Num of Incomplete Nodes')

    # Show the plot
    plt.show()
    

def plot_summary_4v(csv_file):
    df = pd.read_csv(csv_file)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the data points in 3D space, using 'k', 'n', and 'd' as the x, y, and z coordinates, respectively
    # Use color or marker style to represent the 'r' variable
    scatter = ax.scatter(df['k'], df['size'], df['ave_density'], c=df['ave_rate'], cmap='viridis', alpha=0.7)

    # Add labels for each axis
    ax.set_xlabel('# of Connections Per Node')
    ax.set_ylabel('Size')
    ax.set_zlabel('Density')

    # Add a colorbar to represent the 'r' variable
    cbar = plt.colorbar(scatter, label='Average Rate')

    # Show the plot
    plt.show()

def plot_summary_3v(csv_file):
    df = pd.read_csv(csv_file)

    plt.scatter(df['size'], df['ave_rate'], c=df['k'], cmap='viridis', alpha=0.7)
    # plt.scatter(df['k'], df['ave_rate'])

    # Add labels and a colorbar
    plt.xlabel('size')
    plt.ylabel('ave_rate')
    plt.colorbar(label='# connections')
    plt.title('Lattice Network Summary Size vs. Avg Rate, By K')

    plt.show()

def plot_csv_data_k(csv_file, n):
    df = pd.read_csv(csv_file)

    column1 = df.loc[df['size'] == n, 'k']
    column2 = df.loc[df['size'] == n,'ave_rate']
    column3 = df.loc[df['size'] == n,'ave_density']

    # Create a plot
    plt.figure(figsize=(10, 6))
    plt.ylim(0.5, 1.5)
    plt.plot(column1, column2, marker='o', linestyle='-')
    plt.xlabel('# Connections Per Node')
    plt.ylabel('Average Rate')
    plt.title('Lattice Network Size vs. Avg Rate, N = ' + str(n))

    plt.show()

def plot_csv_data_n(csv_file, k):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Assuming the first and second columns are named 'Column1' and 'Column2'
    column1 = df['size']
    column2 = df['ave_rate']
    column3 = df['ave_density']

    # # Create a plot
    # plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    # plt.plot(column1, column2, marker='o', linestyle='-')
    # plt.xlabel('Size')
    # plt.ylabel('Average Rate')
    # plt.title('Lattice Network Size vs. Avg Rate, K = ' + str(k))

    # Use scatter plot with a color map based on the values of 'Column3'
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    scatter = plt.scatter(column1, column2, c=column3, cmap='viridis', marker='o')
    plt.colorbar(scatter, label='density')
    plt.xlabel('Size')
    plt.ylabel('Average Rate')
    plt.title('Lattice Network Size vs. Avg Rate, K = ' + str(k))

    # Show the plot
    # plt.show()
    plt.savefig('lattice_scatter_k' + str(k) + '.png')
    plt.close()

def main():
    filename = "../../data/data_all_lattice_mod_k.csv"
    # plot_mod_4v(filename)
    plot_mod_3v(filename)

    # filename = "../../data/data_all_lattice_k.csv"
    # plot_incomp_4v(filename)
    # plot_summary_4v(filename)

    # for n in range(5, 51):
    #     plot_csv_data_k(filename, n)

    # for k in range(4, 11):
    #     filename = "../../data/data_lattice_k" + str(k) + ".csv"
    #     plot_csv_data_n(filename, k)

if __name__ == "__main__":
    main()