import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any
from pydantic import BaseModel, Field
import csv
import json
from kafka import KafkaProducer, KafkaConsumer

def read_json_file(file_path: str="config/config.json") -> Dict[str, Any] | None:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file_path}': {e}")
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

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

async def send_messege_to_kafka(csv_file: str, kakfk_topic: str) -> None:
    PRODUCER = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    with open(csv_file, mode="r") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            message = {
                'trackID': int(row['trackID']),
                'X': float(row['X']),
                'Y': float(row['Y']),
                'V_X': float(row['V_X']),
                'V_Y': float(row['V_Y'])
            }
            try:
                PRODUCER.send(kakfk_topic, value=message)
            except Exception as error:
                print(f"Can't send messege to topic becuase '{error}'")
    PRODUCER.flush()

def recieve_messege_from_kafka(kafka_topic: str):
    CONSUMER = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',  # Start reading at the earliest message
        enable_auto_commit=True,
        # group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        key_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
    )

    print("Listening for messages...")

    for messege in CONSUMER:
        yield messege.value
    CONSUMER.close()

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
