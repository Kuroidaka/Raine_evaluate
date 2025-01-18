from openai import OpenAI, AsyncOpenAI
from model import MemoryEvaluationClusters
client = AsyncOpenAI(api_key="")
from typing import Dict
import json
from utils import append_to_clustered_json
import logging


async def clustering_dataset(data):
    """
    Processes a dataset to classify entries and append them to a clustered dataset JSON file.

    Args:
        data (dict): A dictionary containing 'tell', 'question', and 'expected' as keys.

    Logs the progress and any errors encountered during the process.
    """
    for i in range(len(data['question'])):
        try:
            logging.info(f"Processing entry {i + 1}/{len(data['question'])}...")

            # Use the loop index `i` to access the correct elements from data
            tell = str(data['tell'][i])
            question = str(data['question'][i])
            expected_answer = str(data['expected'][i])
            logging.debug(f"Extracted data - Tell: {tell}, Question: {question}, Expected: {expected_answer}")

            # Call the classify_with_ai function to get the clustering response
            clustering_response = await classify_with_ai(tell, question, expected_answer)
            logging.debug(f"Clustering response for entry {i + 1}: {clustering_response}")

            # Create a data dictionary to append to the clustered_dataset
            data_entry = {
                "tell": tell,
                "question": question,
                "expected": expected_answer
            }

            # Append the data to the clustered dataset based on the clustering response
            append_to_clustered_json(
                file_path="clustered_dataset.json",
                response=clustering_response,
                data_entry=data_entry
            )
            logging.info(f"Successfully processed entry {i + 1}/{len(data['question'])}.")

        except Exception as e:
            logging.error(f"Error processing entry {i + 1}: {e}")
            raise

        

async def classify_with_ai(tell: str, question: str, expected: str) -> Dict[str, bool]:
    """
    Uses an AI model to classify the dataset entry into predefined clusters.

    Args:
        tell (str): The user's statement containing information.
        question (str): The related question for memory recall.
        expected (str): The expected answer.

    Returns:
        Dict[str, bool]: A dictionary of clusters with boolean values indicating applicability.
    """
    prompt = f"""
    You are an expert in dataset evaluation and clustering for virtual assistant memory. Based on the provided input, classify it into one or more of the following clusters. For each cluster, indicate whether it applies (`true`) or not (`false`).  

    Clusters:
    - Personal_Information: Tests the ability to store and recall basic user details over the long term.
    - Habits_and_Preferences: Verifies if the assistant can remember user habits and preferences.
    - Significant_Events: Evaluates the ability to recall specific past events mentioned by the user.
    - Relationships_and_Connections: Tests memory of information about family, friends, or pets shared by the user.
    - Plans_and_Goals: Checks the ability to remember future plans or aspirations shared by the user.
    - Appointments_and_Time_Specific_Information: Ensures the assistant can accurately recall times and important dates.
    - Ownership_and_Possessions: Tests memory of items or properties owned by the user.
    - Locations_and_Places: Evaluates the ability to remember information about places significant to the user.
    - Contextual_and_Multi_Session_Memory: Tests the ability to connect and recall information across multiple sessions or contexts.

    ### Task:
    Classify the input into the clusters above and provide your clustering in JSON format like this:
    {{
        "Personal_Information": <true/false>,
        "Habits_and_Preferences": <true/false>,
        "Significant_Events": <true/false>,
        "Relationships_and_Connections": <true/false>,
        "Plans_and_Goals": <true/false>,
        "Appointments_and_Time_Specific_Information": <true/false>,
        "Ownership_and_Possessions": <true/false>,
        "Locations_and_Places": <true/false>,
        "Contextual_and_Multi_Session_Memory": <true/false>
    }}
    """
    try:
        response = await client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"""
                    ### Input:
                    TELL: {tell}
                    QUESTION: {question}
                    EXPECTED: {expected}
                """}
            
            ],
            response_format=MemoryEvaluationClusters,
        )
        

        clustering_text = response.choices[0].message.content  # Proper attribute access
        clustering = json.loads(clustering_text) 
        return clustering
    except Exception as e:
        raise