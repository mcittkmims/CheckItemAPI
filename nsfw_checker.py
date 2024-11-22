import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData, ImageCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError


def nsfw_image_checker(image_content, endpoint, api_key):

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))

    request = AnalyzeImageOptions(image=ImageData(content=image_content))

    # Analyze image
    try:
        response = client.analyze_image(request)
    except HttpResponseError as e:
        return {
            "error": "Not Found",
            "message": "Image analysis failed. Please try again later.",
            "code": 500
        }

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

    if not (hate_result.severity or self_harm_result.severity or sexual_result.severity or violence_result.severity):
        return {
            "safe": True,
            "message": "Image is safe.",
            "code": 200
        }

    return {
        "safe": False,
        "message": "Image contains potentially unsafe content.",
        "code": 200
    }

