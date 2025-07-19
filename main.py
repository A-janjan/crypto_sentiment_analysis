from producer import produce_crypto_news
from sentiment_analysis import sentiment_analysis


if __name__ == "__main__":
    produce_crypto_news()
    print("Crypto news production completed.")
    
    sentiment_analysis()
    print("Sentiment analysis completed.")