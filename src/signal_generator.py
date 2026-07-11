class SignalGenerator:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
    
    def generate_signal(self, sentiments):
        """
        sentiments: list of sentiment results from analyzer
        Returns: BUY, SELL, or HOLD
        """
        if not sentiments:
            return "HOLD", 0
        
        # Count sentiments
        positive_count = sum(1 for s in sentiments if s['sentiment'] == 'positive')
        negative_count = sum(1 for s in sentiments if s['sentiment'] == 'negative')
        total = len(sentiments)
        
        # Calculate positive ratio
        positive_ratio = positive_count / total if total > 0 else 0
        
        # Generate signal
        if positive_ratio > self.threshold:
            return "BUY", positive_ratio
        elif positive_ratio < 0.3:
            return "SELL", positive_ratio
        else:
            return "HOLD", positive_ratio