from openai import OpenAI, AsyncOpenAI

client = AsyncOpenAI(api_key="")
import json
from pydantic import BaseModel
import os
import aiohttp
import pandas as pd
import asyncio
from model import EvalResponse, MemoryEvaluationClusters
from cluster_dataset import clustering_dataset
from utils import append_to_clustered_json, load_clustered_json, store_evaluation_result
# Set your OpenAI API key
from evaluate import calc_criteria


def get_dataset(file_path, sheet_name):
        # Load data from Excel
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except FileNotFoundError:
        print("Error: Excel file not found.")
        return
    except KeyError:
        print(f"Error: in sheet '{sheet_name}'.")
        return

async def tell_func(tell_data):
    # Loop through the data and call the API
    for context in tell_data:
        if pd.isna(context):  # Check for empty fields
            print("Skipped empty field.")
            continue

        print(f"Input: {context}")
        # await asyncio.sleep(1)

async def main():
    # file_path = 'data_test.xlsx'  # Replace with the path to your Excel file
    # sheet_name_1 = 'Canh'  # Replace with your sheet name
    # sheet_name_2 = 'random 1'  # Replace with your sheet name
    # sheet_name_3 = 'random2'  # Replace with your sheet name

    # data = get_dataset(file_path, sheet_name_1)
    # data_1 = get_dataset(file_path, sheet_name_2)
    # data_2 = get_dataset(file_path, sheet_name_3)

    # # Combine all datasets into a single list
    # combined_data = pd.concat([data, data_1, data_2], ignore_index=True)

    # Pass the combined data to the clustering function
    # await clustering_dataset(combined_data)

    # clustered_json = load_clustered_json("clustered_dataset.json")  # Load the clustered JSON file

    # # Loop through each cluster key
    # for key, value in clustered_json.items():
    #     if value:  # Process only if the cluster has data
    #         # Calculate criteria for the current cluster
    #         data = await calc_criteria(value, criteria=key)

    #         # Store the evaluation result for the current cluster
    #         store_evaluation_result(file_path="evaluation_results.json", name=key, result=data)
        
        # Append the evaluation to a JSON file

    
    clustered_json = load_clustered_json("evaluation_results.json")  # Load the clustered JSON file
    print(clustered_json)
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

