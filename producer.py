import requests
from dotenv import load_dotenv
from kafka import KafkaProducer
import os
import json

load_dotenv()

API_KEY = os.environ.get("CRYPTOPANIC_API_KEY")

URL = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_KEY}&currencies=ETH"



def produce_crypto_news():
    """
    Fetches the latest crypto news from Cryptopanic and sends it to a Kafka topic.
    """
    if not API_KEY:
        raise ValueError("Cryptopanic API key is not set in the environment variables.")
    if not URL:
        raise ValueError("Cryptopanic API URL is not set.")
    print("Fetching crypto news...")
    # Fetch crypto news
    response = requests.get(URL)
    data = response.json()

    # Initialize Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Send each post to Kafka
    for post in data.get("results", []):
        producer.send('crypto-news', post)

    producer.flush()
    print(f"Sent {len(data.get('results', []))} crypto news posts to Kafka.")
    
if __name__ == "__main__":
    produce_crypto_news()
    print("Done!")