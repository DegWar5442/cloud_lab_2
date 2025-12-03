import requests
import json
import getpass
import os

def summarize_text(api_key, text):
    """
    Summarize text using the facebook/bart-large-cnn model via Hugging Face API.
    """
    API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Check for input length to prevent common 400 errors due to token limits.
    if len(text) > 5000:
        return "Error: Input text is too long (over 5000 characters). Please shorten it."
        
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 130, # Max length of the generated summary
            "min_length": 30,  # Min length of the generated summary
            "do_sample": False # Ensures deterministic output
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        # Handle authorization and bad request errors directly
        if response.status_code == 401:
             return "Error 401: Unauthorized. Please check your Hugging Face API key."
        elif response.status_code == 400:
             # Handles issues like unsupported language or excessive payload size.
             return f"Error 400: Bad Request. Possible issues: text too long or unsupported language. Details: {response.text}"
        
        response.raise_for_status()
        
        result = response.json()
        
        # Parse the summary from the expected list or dict structure
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('summary_text', 'No summary generated.')
        elif isinstance(result, dict) and 'summary_text' in result:
            return result['summary_text']
        elif isinstance(result, dict) and 'error' in result:
            return f"API Error: {result['error']}"
        else:
            return f"Unexpected response format: {result}"
            
    except requests.exceptions.RequestException as e:
        return f"Request failed: Network or connection error ({str(e)})"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def display_stats(original_text, summary_text):
    """
    Display compression statistics (character count and percentage reduction).
    """
    original_chars = len(original_text)
    summary_chars = len(summary_text)
    compression_rate = ((1 - (summary_chars / original_chars)) * 100) if original_chars > 0 else 0
    
    print()
    print("=" * 60)
    print("COMPRESSION STATISTICS")
    print("=" * 60)
    print(f"Original Characters:     {original_chars:,}")
    print(f"Summary Characters:      {summary_chars:,}")
    print(f"Compression Rate:        {compression_rate:.1f}%")
    print(f"Summary is {compression_rate:.1f}% shorter than original")
    print("=" * 60)


def main():
    print("=" * 60)
    print("BART Text Summarizer")
    print("Using facebook/bart-large-cnn model from Hugging Face")
    print("=" * 60)
    print()
    
    # 1. Check environment variable for the API key (Secure practice)
    api_key = os.environ.get("HF_API_KEY")
    
    if not api_key:
        print("INFO: API key not found in environment variable 'HF_API_KEY'. Requesting input.")
        # 2. If not found, request hidden input using getpass
        try:
            api_key = getpass.getpass("Enter your Hugging Face API key (input is hidden): ").strip()
        except Exception:
            # Fallback input method if getpass fails
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
        
        # Read multi-line input until an empty line is entered
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

        # Final check before API call
        if len(text) > 5000:
             print("Error: Input text is too long (over 5000 characters). Please shorten it.")
             continue

        print()
        print("Summarizing...")
        print("-" * 60)
        
        summary = summarize_text(api_key, text)
        
        print()
        print("SUMMARY:")
        print(summary)
        print("-" * 60)
        
        # Display stats only on successful summarization
        if not summary.startswith("Error:") and not summary.startswith("Request failed:") and not summary.startswith("API Error:"):
            display_stats(text, summary)
        
        print()
        print("Enter more text to summarize, or type 'quit' to exit:")


if __name__ == "__main__":
    main()
