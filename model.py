import re
from transformers import pipeline # type: ignore
class Summarizer:
    def __init__(self,):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)
    
    def infer(self, text):
        # Splitting text into chunks (max 1024 characters per chunk)
        chunk_size = 1024
        article_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        # Summarize each chunk
        summaries = self.summarizer(article_chunks, max_length=60, min_length=20, do_sample=False, batch_size=8)
        summaries = [summary['summary_text'] for summary in summaries]

        # Combine all summaries
        final_summary = " ".join(summaries)
        return final_summary