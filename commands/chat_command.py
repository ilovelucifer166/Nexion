from collections import deque
import requests
import random
import time

def generate_response(user_id, prompt, config, history):  # Added history parameter
    # Added API key rotation and rate limit handling
    api_keys = config['OPENROUTER_API_KEYS']  # Now expects list of keys
    random.shuffle(api_keys)  # Distribute load evenly

    messages = [{"role": "system", "content": config['SYSTEM_PROMPT']}]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": config['MODEL'],
        "messages": messages,
        "temperature": 1.0,
    }

    for idx, api_key in enumerate(api_keys):
        try:
            headers["Authorization"] = f"Bearer {api_key}"

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:  # Rate limited
                if idx < len(api_keys) - 1:
                    time.sleep(1.5 ** (idx + 1))  # Exponential backoff
                    continue
                return "Rate limit exceeded on all API keys. Please try again later."
            return f"API Error: {str(e)}"

        except Exception as e:
            if idx == len(api_keys) - 1:  # Last key failed
                return f"Error generating response: {str(e)}"
            time.sleep(0.5)

    return "All API keys exhausted. Please try again later."
