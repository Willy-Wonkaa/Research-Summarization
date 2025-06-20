import requests
import os
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
headers = {
        "Authorization": f"Bearer {os.getenv("HF_TOKEN")}"  # Replace with your token
        }
class Summarizer:   
    def infer(self, text):
        # Splitting text into chunks (max 1024 characters per chunk)
        payload = {
        "inputs": text,
        "parameters": {
            "clean_up_tokenization_spaces": True,
            "truncation": "longest_first",
            "min_length": 20,
            "max_length": 60,
            "do_sample": False
        }
    }
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        return result[0]['summary_text']
    
    def summarize_article(self,text, chunk_size=1024):
        article_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        summaries = [self.infer(chunk) for chunk in article_chunks]
        return " ".join(summaries)