import os
import requests

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData, ImageCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv


def nsfw_image_checker(image_url, endpoint, api_key):

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        image_content = response.content
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image from URL: {e}")
        raise

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))

    request = AnalyzeImageOptions(image=ImageData(content=image_content))

    # Analyze image
    try:
        response = client.analyze_image(request)
    except HttpResponseError as e:
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(item for item in response.categories_analysis if item.category == ImageCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == ImageCategory.VIOLENCE)

    if hate_result:
        print(f"Hate severity: {hate_result.severity}")
    if self_harm_result:
        print(f"SelfHarm severity: {self_harm_result.severity}")
    if sexual_result:
        print(f"Sexual severity: {sexual_result.severity}")
    if violence_result:
        print(f"Violence severity: {violence_result.severity}")


load_dotenv()
nsfw_image_checker('https://static1.dualshockersimages.com/wordpress/wp-content/uploads/2023/12/tamaki-from-fire-force.jpg', os.getenv('CONTENT_SAFETY_ENDPOINT'), os.getenv('CONTENT_SAFETY_KEY'))
