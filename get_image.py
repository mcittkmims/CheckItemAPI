import requests


def fetch_image(image_url):

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image from URL: {e}")
        raise ValueError("Unable to download the image. Please check the URL and try again.") from e



