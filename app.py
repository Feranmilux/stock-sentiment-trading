import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from news_scraper import NewsScraper
from sentiment_analyzer import SentimentAnalyzer
from signal_generator import SignalGenerator

st.set_page_config(page_title="Stock Sentiment Analyzer", layout="wide")

st.title("📈 Stock Sentiment Trading System")
st.markdown("*Uses FinBERT to analyze financial news and generate trading signals*")

# Sidebar
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("NewsAPI Key", type="password")

stocks = st.sidebar.multiselect(
    "Select stocks to analyze",
    ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "META"],
    default=["AAPL", "MSFT"]
)

sentiment_threshold = st.sidebar.slider(
    "Sentiment threshold for BUY signal",
    min_value=0.3,
    max_value=0.9,
    value=0.5
)

st.markdown("---")

if not api_key:
    st.warning("⚠️ Please enter your NewsAPI key in the sidebar to continue")
    st.info("""
    Don't have a NewsAPI key?
    1. Go to https://newsapi.org
    2. Sign up for free
    3. Copy your API key
    4. Paste it in the sidebar
    """)
else:
    if st.button("🔍 Analyze Now", key="analyze_btn"):
        st.markdown("---")
        
        scraper = NewsScraper(api_key)
        analyzer = SentimentAnalyzer()
        generator = SignalGenerator(sentiment_threshold)
        
        results = {}
        
        for stock in stocks:
            with st.spinner(f"Analyzing {stock}..."):
                articles = scraper.get_stock_news(stock)
                texts = scraper.extract_text(articles)
                
                if not texts:
                    st.warning(f"No news found for {stock}")
                    continue
                
                sentiments = []
                for text in texts:
                    result = analyzer.analyze(text)
                    sentiments.append(result)
                
                signal, ratio = generator.generate_signal(sentiments)
                results[stock] = {
                    "signal": signal,
                    "ratio": ratio,
                    "sentiments": sentiments,
                    "articles": articles
                }
        
        st.markdown("### 📊 Results")
        
        cols = st.columns(len(results))
        for idx, (stock, data) in enumerate(results.items()):
            with cols[idx]:
                signal = data['signal']
                ratio = data['ratio']
                color = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"
                
                st.metric(
                    label=stock,
                    value=f"{color} {signal}",
                    delta=f"{ratio:.1%} positive"
                )
        
        st.markdown("---")
        
        for stock, data in results.items():
            with st.expander(f"📄 {stock} - Sentiment Details"):
                sentiments = data['sentiments']
                
                positive = sum(1 for s in sentiments if s['sentiment'] == 'positive')
                negative = sum(1 for s in sentiments if s['sentiment'] == 'negative')
                neutral = sum(1 for s in sentiments if s['sentiment'] == 'neutral')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🟢 Positive", positive)
                with col2:
                    st.metric("🟡 Neutral", neutral)
                with col3:
                    st.metric("🔴 Negative", negative)
                
                st.write(f"\n**Recent Articles ({len(data['articles'])} total):**")
                for article in data['articles'][:5]:
                    st.write(f"- {article['title'][:80]}...")
                    st.write(f"  *Source: {article['source']['name']}*")

st.markdown("---")
st.markdown("*Built with FinBERT • Updated daily*")