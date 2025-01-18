import os
import json
from typing import Any

def append_to_clustered_dataset(response: dict, data: dict, clustered_dataset: dict) -> None:

    for cluster, is_true in response.items():
        if is_true:
            clustered_dataset[cluster].append(data)

def append_to_json_file(new_data: Any, file_path='evaluations.json'):
    """
    Appends new data to a JSON file. If the file does not exist, it creates one.
    :param file_path: Path to the JSON file.
    :param new_data: Data to append, must be a dictionary.
    """
    if not isinstance(new_data, dict):
        raise ValueError("new_data must be a dictionary.")

    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("JSON file must contain a list at the root.")
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append the new data
    data.append(new_data)

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def append_to_clustered_json(file_path: str, response: dict, data_entry: dict) -> None:
    """
    Appends a data entry to the appropriate clusters in a JSON file based on the response.
    Creates a cluster if it does not already exist.

    Args:
        file_path (str): Path to the JSON file.
        response (dict): A dictionary with cluster names as keys and boolean values indicating where to append.
        data_entry (dict): The data to append, containing "tell", "question", and "expected".
    """
    try:
        # Load the existing JSON file
        try:
            with open(file_path, "r") as file:
                clustered_dataset = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty dictionary
            clustered_dataset = {}

        # Update the appropriate clusters
        for cluster, is_true in response.items():
            if is_true:
                if cluster not in clustered_dataset:
                    clustered_dataset[cluster] = []  # Create the cluster if it doesn't exist
                clustered_dataset[cluster].append(data_entry)

        # Save the updated dataset back to the file
        with open(file_path, "w") as file:
            json.dump(clustered_dataset, file, indent=4)

    except json.JSONDecodeError:
        print("Error: The JSON file is improperly formatted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def load_clustered_json(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} does not exist.")
        raise
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not a valid JSON file.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    
def calculate_average_scores(data: list) -> dict:
    """
    Calculates the average of numerical fields (Accuracy, Relevance, Coherence, Fluency) in the dataset
    and rounds the results to two decimal places.

    Args:
        data (list): A list of dictionaries containing numerical fields and comments.

    Returns:
        dict: A dictionary with the average scores for each numerical field, rounded to two decimal places.
    """
    if not data:
        return {"Accuracy": 0.00, "Relevance": 0.00, "Coherence": 0.00, "Fluency": 0.00}

    # Initialize totals
    totals = {"Accuracy": 0, "Relevance": 0, "Coherence": 0, "Fluency": 0}

    # Sum up the values
    for entry in data:
        for key in totals.keys():
            totals[key] += entry.get(key, 0)

    # Calculate averages and round to two decimal places
    num_entries = len(data)
    averages = {key: round(totals[key] / num_entries, 2) for key in totals}

    return averages


def store_evaluation_result(name: str, result: dict, file_path="evaluation_result") -> None:
    try:
        # Load existing data from the file, or initialize an empty list if the file does not exist
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        # Update or append the result for the given criterion
        updated = False
        for entry in data:
            if entry["name"] == name:
                entry["result"] = result
                updated = True
                break
        
        if not updated:
            data.append({"name": name, "result": result})

        # Write the updated data back to the file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        print(f"An error occurred while storing the evaluation result: {e}")

def add_to_json_file(category: str, dataset: dict, evaluate: dict, file_path = "evaluation_result_detail.json") -> None:

    try:
        # Load the existing JSON data or initialize an empty dictionary if the file doesn't exist
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            json_data = {}

        # Ensure the category exists in the JSON structure
        if category not in json_data:
            json_data[category] = []

        # Add the new entry to the category
        json_data[category].append({"dataset": dataset, "evaluate": evaluate})

        # Write the updated data back to the file
        with open(file_path, "w") as file:
            json.dump(json_data, file, indent=4)

    except json.JSONDecodeError:
        print("Error: The JSON file is not properly formatted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
