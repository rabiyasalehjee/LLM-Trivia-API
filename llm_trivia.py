import subprocess
import json
import re
import logging
import time  


logging.basicConfig(filename="llm.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_json(response_text):
    """
    Extracts a JSON object from the LLM response text.
    """
    
    start_index = response_text.find('{')
    if start_index == -1:
        logging.error("No JSON object found in response.")
        logging.error(f"Raw response: {response_text}")
        return None
    
    json_text = response_text[start_index:]
    try:
        logging.info("Extracting JSON from response.")
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")
        logging.error(f"Raw response: {response_text}")
        return None

def get_trivia_question():
    """
    Generates a trivia question using the LLM and returns it as a JSON object.
    """
    prompt = """
    Generate a trivia question with 4 multiple-choice answers.
    Return ONLY a valid JSON object, with no extra text.

    Format:
    {
        "question": "...",
        "options": ["...", "...", "...", "..."],
        "correctAnswer": "..."
    }
    """
    logging.info("Sending prompt to LLM...")
    
    command = ["ollama", "run", "deepseek-r1:1.5b", prompt]
    
    for attempt in range(3):
        try:
            response = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', check=False, timeout=120)
            
            if response.returncode == 0:
                logging.info("LLM Response received successfully.")
                logging.info(f"Raw LLM response: {response.stdout.strip()}")  
                extracted_data = extract_json(response.stdout.strip())
                if extracted_data:
                    logging.info(f"Extracted Trivia JSON: {extracted_data}")
                    return extracted_data
                else:
                    logging.warning(f"Attempt {attempt + 1}: Invalid JSON, retrying...")
            else:
                logging.error(f"LLM execution failed with error: {response.stderr.strip()}")
        except Exception as e:
            logging.error(f"Exception occurred while running LLM: {str(e)}")
        
        time.sleep(2)  

    
    logging.error("All attempts failed. Returning fallback question.")
    return {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "correctAnswer": "Paris"
    }

if __name__ == '__main__':
    question = get_trivia_question()
    print(json.dumps(question))  