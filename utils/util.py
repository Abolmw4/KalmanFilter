import matplotlib.pyplot as plt
from typing import List, Tuple
from pydantic import BaseModel, Field


class Radar(BaseModel):
    X: float = Field(title="X cartesian position")
    Y: float = Field(title="Y cartesian position")
    V_X: float = Field(title="V_X speed in X direction", gt=0)
    V_Y: float = Field(title="V_Y speed in Y direction", gt=0)

class RadarInfo(BaseModel):
    Id: int
    radar_info: Radar

class EstimateInfo(BaseModel):
    Id: int
    X: float
    Y: float

class Response(BaseModel):
    Id: int
    x: float
    Y: float

def plot(points: List[Tuple]):
    x_vals, y_vals = zip(*points)

    # Plot the line
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='b', label='real')

    # Add labels and title
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Line Plot from Points')
    plt.legend()
    plt.grid(True)

    # Save or show the plot
    plt.savefig("line_plot.png")  # For headless environments


def plot_two_lines(points1: List[Tuple], points2: List[Tuple]):
    x1, y1 = zip(*points1)
    x2, y2 = zip(*points2)

    plt.figure()

    # First line: real points
    plt.plot(x1, y1, marker='o', linestyle='-', color='b', label='Real')

    # Second line: predicted or other points
    plt.plot(x2, y2, marker='x', linestyle='--', color='r', label='Predicted')

    # Labels and layout
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Real vs Predicted Trajectories')
    plt.legend()
    plt.grid(True)

    # Save the plot (headless safe)
    plt.savefig("line_plot.png")


def plot_three_lines(points1: List[Tuple], points2: List[Tuple], points3: List[Tuple]):
    x1, y1 = zip(*points1)
    x2, y2 = zip(*points2)
    x3, y3 = zip(*points3)

    plt.figure()

    # First line: real points
    plt.plot(x1, y1, marker='o', linestyle='-', color='b', label='Real')

    # Second line: predicted or other points
    plt.plot(x2, y2, marker='x', linestyle='--', color='r', label='Noisy')

    plt.plot(x3, y3, marker='s', linestyle='-.', color='g', label='Predicted')

    # Labels and layout
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Real vs Noisy vs Predicted')
    plt.legend()
    plt.grid(True)

    # Save the plot (headless safe)
    plt.savefig("line_plot.png")

