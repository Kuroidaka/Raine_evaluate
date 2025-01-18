from openai import OpenAI, AsyncOpenAI

client = AsyncOpenAI(api_key="")
import aiohttp
# Set your OpenAI API key
import os

# Make sure you have set the environment variable "TOKEN" beforehand
token = ""

if token:
    print("Token retrieved successfully!")
else:
    print("Token not found. Please set the TOKEN environment variable.")

async def call_app_api(context):
    api_url = "http://localhost:8001/api/v2/brain/chat?isStream=false&isLTMemo=true"  
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"  # Ensure correct content type is set
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(api_url, json={"prompt": context}, headers=headers) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                data = await response.json()

                # Extract the "lastMessage" field, raise an error if it's missing
                if "lastMessage" not in data:
                    raise KeyError("'lastMessage' not found in the API response")

                return data["lastMessage"]

        except aiohttp.ClientResponseError as e:
            # Raised for 4xx or 5xx HTTP status codes
            raise RuntimeError(f"HTTP error while calling app API: {e.status} {e.message}")
        except aiohttp.ClientError as e:
            # Raised for network-related issues
            raise RuntimeError(f"Network error while calling app API: {str(e)}")
        except KeyError as e:
            # Raised when expected key is missing in the response
            raise RuntimeError(f"Invalid API response: {str(e)}")
        except Exception as e:
            # Handle any other unforeseen exceptions
            raise RuntimeError(f"An unexpected error occurred: {str(e)}")
