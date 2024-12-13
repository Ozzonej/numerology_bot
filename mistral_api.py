import requests

def get_interpretation(query, api_key):
    """
    Get interpretation from Chat.Mistral.AI API.
    :param query: The query to send to the API
    :param api_key: The API key for authentication
    :return: Interpretation result
    """
    url = "https://api.mistral.ai/v1/chat/completions"  # Updated to a more common endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-large-latest",  # Add model parameter if required
        "messages": [{"role": "user", "content": query}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
