import matplotlib.pyplot as plt
import numpy as np
from utils import load_clustered_json

def plot_radar_chart(data):
    # Metrics to be plotted
    metrics = ["Accuracy", "Relevance", "Coherence", "Fluency"]
    categories = [item["name"] for item in data]  # Names of the categories
    
    # Normalize data for radar chart
    num_metrics = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist() + [0]  # Angles for the radar

    # Create a radar chart for each category
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
    for item in data:
        values = [item["result"][metric] for metric in metrics]
        values += values[:1]  # Repeat the first value to close the circle
        ax.plot(angles, values, label=item["name"])
        ax.fill(angles, values, alpha=0.25)

    # Customize the radar chart
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], color="gray")
    ax.set_ylim(0, 10)
    ax.set_title("Radar Chart of Evaluation Results", fontsize=16)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.show()

def plot_grouped_bar_chart_scientific(data):
    # Metrics to plot
    metrics = ["Accuracy", "Relevance", "Coherence", "Fluency"]
    categories = [item["name"] for item in data]  # Names of categories

    # Extract values for each metric
    metric_values = {metric: [item["result"][metric] for item in data] for metric in metrics}

    # Set bar positions
    x = np.arange(len(categories))  # Positions for categories
    bar_width = 0.2  # Width of each bar

    # Set up figure and axis
    plt.figure(figsize=(10, 6))  # Adjust figure size for clarity
    for i, metric in enumerate(metrics):
        plt.bar(
            x + i * bar_width,  # Offset bars for grouping
            metric_values[metric],  # Values for the metric
            bar_width,  # Bar width
            label=metric  # Add legend label
        )

    # Customize x-axis and y-axis
    plt.xticks(x + bar_width * (len(metrics) - 1) / 2, categories, rotation=45, fontsize=10, ha="right")
    plt.yticks(fontsize=10)
    plt.ylabel("Scores", fontsize=12)
    plt.xlabel("Categories", fontsize=12)
    plt.ylim(0, 10)  # Ensure uniform y-axis for comparison

    # Add title and legend
    plt.title("Evaluation Metrics by Category", fontsize=14, fontweight="bold")
    plt.legend(title="Metrics", fontsize=10, title_fontsize=12, loc="upper left", bbox_to_anchor=(1.05, 1))

    # Add gridlines
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Save the plot as a high-resolution image
    plt.tight_layout()
    plt.savefig("grouped_bar_chart.png", dpi=300)  # Save as high-resolution PNG
    plt.show()
def plot_line_chart_scientific(data):
    # Metrics to plot
    metrics = ["Accuracy", "Relevance", "Coherence", "Fluency"]
    categories = [item["name"] for item in data]  # Names of categories

    # Extract values for each metric
    metric_values = {metric: [item["result"][metric] for item in data] for metric in metrics}

    # Setup figure and axis
    plt.figure(figsize=(8, 5))  # Set size appropriate for papers
    for metric, values in metric_values.items():
        plt.plot(
            categories, 
            values, 
            marker="o",  # Use markers for visibility in grayscale
            linewidth=2,  # Line thickness
            label=metric  # Label for legend
        )

    # Add title and labels
    plt.title("Evaluation Metrics Across Categories", fontsize=14, fontweight='bold')
    plt.xlabel("Categories", fontsize=12)
    plt.ylabel("Scores", fontsize=12)

    # Customize ticks
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)

    # Add gridlines
    plt.grid(True, linestyle="--", alpha=0.6)

    # Add legend
    plt.legend(title="Metrics", fontsize=10, title_fontsize=12, loc="upper left", bbox_to_anchor=(1.05, 1))

    # Tight layout for papers
    plt.tight_layout()
    plt.savefig("evaluation_line_chart.png", dpi=300)  # Save as high-resolution PNG
    plt.show()

# Example data
data = load_clustered_json("evaluation_results.json")
plot_grouped_bar_chart_scientific(data)
