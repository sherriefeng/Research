import networkx as nx
import random
import csv
from itertools import combinations, groupby
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_data(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Assuming the first and second columns are named 'Column1' and 'Column2'
    column1 = df['size']
    column2 = df['ave_rate']

    # Create a plot
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.plot(column1, column2, marker='o', linestyle='-')
    plt.xlabel('Size')
    plt.ylabel('Average Rate')
    plt.title('Plot of Size vs. Avg Rate')

    # Show the plot
    plt.show()

def main():
    filename = "../../data/data_summary_random.csv"
    plot_csv_data(filename)

if __name__ == "__main__":
    main()