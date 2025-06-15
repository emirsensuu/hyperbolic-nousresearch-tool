import requests
import http.client
import json
import random
import time
import os
from datetime import datetime

# --- API Keys and Settings ---
# It's recommended to set API keys as environment variables for security.
# You can add these in the "Environment Variables" section on Railway.
HYPERBOLIC_API_KEY = os.getenv("HYPERBOLIC_API_KEY")
NOUS_API_KEY = os.getenv("NOUS_API_KEY")

# Hyperbolic API URL and model
HYPERBOLIC_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
HYPERBOLIC_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"

# Nous Research API host and models
NOUS_API_HOST = "inference-api.nousresearch.com"
NOUS_MODELS = [
    "DeepHermes-3-Mistral-24B-Preview",
    "Hermes-3-Llama-3.1-70B",
    "DeepHermes-3-Llama-3-8B-Preview",
    "Hermes-3-Llama-3.1-405B"
]

# --- Configuration ---
COOLDOWN_SECONDS = 30
MAX_TOKENS_HYPERBOLIC = 128  # Reduced for cost optimization
MAX_TOKENS_NOUS = 256       # Reduced for cost optimization

def log_interaction(question, model, answer):
    """Log the interaction with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"""
=== {timestamp} ===
Question: {question}
Model: {model}
Answer: {answer}
{'='*50}
"""
    print(log_entry)
    # Also save to a file
    with open("interactions.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

def get_random_question_from_hyperbolic():
    """Generates a random question using the Hyperbolic API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HYPERBOLIC_API_KEY}"
    }
    
    topics = [
        "physics", "history", "philosophy", "technology", "art", 
        "daily life", "future predictions", "ethical dilemmas", 
        "science fiction", "nature", "space", "health",
        "artificial intelligence", "climate change", "economics",
        "psychology", "mathematics", "literature", "music",
        "sports", "politics", "religion", "education"
    ]
    random_topic = random.choice(topics)

    prompts = [
        f"Generate a short question about {random_topic}.",
        f"Ask a simple question about {random_topic}.",
        f"Create a brief question about {random_topic}.",
        f"Formulate a quick question about {random_topic}."
    ]
    random_prompt = random.choice(prompts)

    data = {
        "messages": [
            {"role": "system", "content": "You are a question generator. Generate very short questions."},
            {"role": "user", "content": random_prompt}
        ],
        "model": HYPERBOLIC_MODEL,
        "max_tokens": MAX_TOKENS_HYPERBOLIC,
        "temperature": 0.9,
        "top_p": 0.9
    }

    try:
        response = requests.post(HYPERBOLIC_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        question = response_json['choices'][0]['message']['content'].strip()
        return question
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Error: Invalid API key for Hyperbolic. Please check your API key in Railway environment variables.")
        else:
            print(f"HTTP Error in Hyperbolic API: {str(e)}")
        return None
    except Exception as e:
        print(f"Error in Hyperbolic API: {str(e)}")
        return None

def ask_nous_model(model_name, question):
    """Asks the specified Nous Research model a question and returns the answer."""
    conn = http.client.HTTPSConnection(NOUS_API_HOST)
    
    payload = json.dumps({
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant. Answer briefly."},
            {"role": "user", "content": question}
        ],
        "max_tokens": MAX_TOKENS_NOUS
    })

    headers = {
        'Authorization': f"Bearer {NOUS_API_KEY}",
        'Content-Type': "application/json"
    }

    try:
        conn.request("POST", "/v1/chat/completions", payload, headers)
        res = conn.getresponse()
        data = res.read()
        response_json = json.loads(data.decode("utf-8"))
        answer = response_json['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        print(f"Error in Nous API: {str(e)}")
        return None
    finally:
        conn.close()

def main():
    """Main loop: Generates unique questions for each model."""
    print("Starting AI Question-Answer System...")
    print(f"Available Nous Models: {', '.join(NOUS_MODELS)}")
    print(f"Cooldown period: {COOLDOWN_SECONDS} seconds")
    print("="*50)

    while True:
        try:
            # Process one model at a time
            for model in NOUS_MODELS:
                # Generate a unique question for this model
                question = get_random_question_from_hyperbolic()
                if not question:
                    print(f"Failed to generate question for {model}, skipping...")
                    continue

                # Get answer from the current model
                answer = ask_nous_model(model, question)
                if answer:
                    log_interaction(question, model, answer)
                else:
                    print(f"Failed to get answer from {model}")

                # Wait before processing the next model
                print(f"\nWaiting {COOLDOWN_SECONDS} seconds before next model...")
                time.sleep(COOLDOWN_SECONDS)

        except KeyboardInterrupt:
            print("\nStopping the system...")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            time.sleep(COOLDOWN_SECONDS)

if __name__ == "__main__":
    main()
