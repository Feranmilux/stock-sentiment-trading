from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAnalyzer:
    def __init__(self):
        # Use FinBERT - trained on financial data
        self.model_name = "ProsusAI/finbert"
        
        print("Loading FinBERT model (first time takes ~2 mins)...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        print("Model loaded!")
    
    def analyze(self, text):
        """Analyze sentiment of financial text"""
        try:
            # Truncate text if too long
            text = text[:512]
            
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
            outputs = self.model(**inputs)
            scores = outputs.logits.softmax(dim=1)
            
            labels = ["negative", "neutral", "positive"]
            sentiment_idx = torch.argmax(scores).item()
            sentiment = labels[sentiment_idx]
            confidence = scores[0][sentiment_idx].item()
            
            return {
                "sentiment": sentiment,
                "confidence": round(confidence, 3),
                "all_scores": {
                    "negative": round(scores[0][0].item(), 3),
                    "neutral": round(scores[0][1].item(), 3),
                    "positive": round(scores[0][2].item(), 3)
                }
            }
        except Exception as e:
            return {"sentiment": "error", "confidence": 0, "error": str(e)}