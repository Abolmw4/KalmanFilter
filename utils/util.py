import matplotlib.pyplot as plt
from typing import List, Tuple
import asyncio

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

async def my_function(name: str, age: int):
    await your_function(age)
    print("finished")

async def your_function(age: int):
    print(f"your age is {age}")


if __name__ == "__main__":
    asyncio.gather(my_function("Abolfazl", 27), your_function(27))
