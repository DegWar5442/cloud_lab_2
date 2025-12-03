import requests
import json

def summarize_text(api_key, text):
    """
    Summarize text using the facebook/bart-large-cnn model via Hugging Face API.
    
    Args:
        api_key (str): Your Hugging Face API key
        text (str): The text to summarize
    
    Returns:
        str: The summarized text or error message
    """
    # Updated API endpoint - using the new router
    API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 130,
            "min_length": 30,
            "do_sample": False
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Handle the response format
        if isinstance(result, list) and len(result) > 0:
            summary = result[0].get('summary_text', '')
            return summary
        elif isinstance(result, dict):
            # Check for summary_text directly in dict
            if 'summary_text' in result:
                return result['summary_text']
            elif 'error' in result:
                return f"Error: {result['error']}"
        else:
            return f"Unexpected response format: {result}"
            
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def main():
    print("=" * 60)
    print("BART Text Summarizer")
    print("Using facebook/bart-large-cnn model from Hugging Face")
    print("=" * 60)
    print()
    
    # Get API key from user
    api_key = input("Enter your Hugging Face API key: ").strip()
    
    if not api_key:
        print("Error: API key cannot be empty!")
        return
    
    print()
    print("Enter the text you want to summarize.")
    print("(Press Enter twice when done, or type 'quit' to exit)")
    print("-" * 60)
    
    while True:
        lines = []
        print()
        
        while True:
            line = input()
            if line.lower() == 'quit':
                print("Goodbye!")
                return
            if line == "" and len(lines) > 0:
                break
            if line:
                lines.append(line)
        
        text = " ".join(lines)
        
        if not text.strip():
            print("Error: Text cannot be empty!")
            continue
        
        print()
        print("Summarizing...")
        print("-" * 60)
        
        summary = summarize_text(api_key, text)
        
        print()
        print("SUMMARY:")
        print(summary)
        print("-" * 60)
        print()
        print("Enter more text to summarize, or type 'quit' to exit:")


if __name__ == "__main__":
    main()