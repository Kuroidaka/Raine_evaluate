from openai import AsyncOpenAI
import logging
client = AsyncOpenAI(api_key="")
import json
import pandas as pd
from model import EvalResponse, MemoryEvaluationClusters
from cluster_dataset import clustering_dataset
from utils import append_to_clustered_json, add_to_json_file, calculate_average_scores
from app_api import call_app_api

async def evaluate_response(context, response, expected_answer):
    prompt = f"""
    You are an evaluator for AI-generated text. Based on the following criteria, rate the response from 1 to 10 for each:
    1. Accuracy: Compare the response to the expected answer. Is the response factually correct?  
    2. Relevance: Does the response address the query effectively?  
    3. Coherence: Is the response logically organized and easy to understand?  
    4. Fluency: Does the response use natural and grammatically correct language?  
    """

    if context:
        prompt += f"Context: {context}\n"

    prompt += f"""
    Response: {response}  
    Expected Answer: {expected_answer}  

    Provide your evaluation in JSON format:
    {{
        "Accuracy": <value from 1 to 10>,
        "Relevance": <value from 1 to 10>,
        "Coherence": <value from 1 to 10>,
        "Fluency": <value from 1 to 10>,
        "Comments": "<additional feedback or explanation>"
    }}
    """
    try:
        # Call the OpenAI API asynchronously
        api_response = await client.beta.chat.completions.parse(
            model="gpt-4o",  # Use the correct model name
            messages=[{"role": "system", "content": prompt}],
            max_tokens=500,
            temperature=0,
            response_format=EvalResponse,
        )
        # Extract the evaluation from the response
        evaluation_text = api_response.choices[0].message.content
        print("evaluation_text", evaluation_text)

        # Parse the JSON response from the model
        evaluation = json.loads(evaluation_text)
        return evaluation
    except Exception as e:
        return {"error": str(e)}

async def tell_func(tell_data):
    # Loop through the data and call the API
    if pd.isna(tell_data):  # Check for empty fields
        print("Skipped empty field.")
        return

    response = await call_app_api(tell_data)

async def calc_criteria(data, criteria):
    eval_list_data = []

    try:
        for item in data:
            try:
                await tell_func(item['tell'])
                eval_item_data = await eval_process(item['question'], item['expected'])
                add_to_json_file(category=criteria , dataset=item, evaluate=eval_item_data,)
                eval_list_data.append(eval_item_data)
            except ValueError as ve:
                logging.warning(f"Validation error for item {item}: {ve}")
            except RuntimeError as re:
                logging.error(f"Runtime error for item {item}: {re}")
            except Exception as e:
                logging.error(f"Unexpected error for item {item}: {e}")

        # Calculate average scores
        eval_data = calculate_average_scores(eval_list_data)
        return eval_data

    except Exception as e:
        logging.critical(f"An unexpected error occurred during calc_criteria: {e}")
        raise


async def eval_process(question: str, expected_answer: str) -> dict:
    try:
        logging.info("Starting evaluation process for question.", question)
        
        # Make the API call
        response = await call_app_api(question)
        logging.info(f"API response received: {response}")

        # Check if the API response is valid
        if not response:
            logging.warning("Empty response from the API.")
            raise ValueError("API response is empty or invalid.")

        # Evaluate the response
        evaluation = await evaluate_response(
            context=question,
            response=response,
            expected_answer=expected_answer
        )
        logging.info(f"Evaluation completed successfully: {evaluation}")
        
        return evaluation

    except ValueError as e:
        logging.error(f"Validation error during the evaluation process: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred during the evaluation process: {e}")
        raise RuntimeError(f"Unexpected error: {str(e)}")
