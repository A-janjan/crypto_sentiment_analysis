from transformers import pipeline # type: ignore
from kafka import KafkaConsumer, TopicPartition
import json



def sentiment_analysis():
    """    Reads the latest crypto news from a Kafka topic and performs sentiment analysis on the titles and descriptions.
    """
    print("Starting sentiment analysis...")
    sentiment_analyzer = pipeline("sentiment-analysis") # type: ignore


    TOPIC = 'crypto-news'
    BOOTSTRAP_SERVERS = 'localhost:9092'
    N_LAST_MESSAGES = 20


    consumer = KafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=None,  # avoid committing offsets
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    # Get partition info (assuming 1 partition, adjust if more)
    tp = TopicPartition(TOPIC, 0)
    consumer.assign([tp])  # manually assign

    # Find the end offset (latest position)
    end_offset = consumer.end_offsets([tp])[tp]


    # Compute where to start (last 10 messages or beginning)
    start_offset = max(end_offset - N_LAST_MESSAGES, 0)
    consumer.seek(tp, start_offset)

    print(f"Reading last {N_LAST_MESSAGES} messages from '{TOPIC}'...")

    count = 0
    total_score = 0.0
    for message in consumer:
        post = message.value
        title = post.get('title', '')
        body = post.get('description', '') or ''

        text = f"{title}. {body}"
        if not text.strip():
            continue

        result = sentiment_analyzer(text)[0]

        
        if result['label'] == 'NEGATIVE':
            total_score -= result['score']
        else:
            total_score += result['score']       
        
        print(f"Title: {title}")
        print(f"Sentiment: {result['label']} (score: {result['score']:.4f})")
        print("="*60)
        
        count += 1
        if count >= N_LAST_MESSAGES:
            break  # Stop after reading N messages


    print(f"Processed {count} messages.")
    
    print()
    print()
    print("#"*60)

    final_score = total_score / count if count > 0 else 0.0
    print(f"Average sentiment score for the last {count} messages: {final_score:.4f}")
    if final_score > 0:   
        print("Overall sentiment is positive.")
    else:
        print("Overall sentiment is negative.")

    print("#"*60)
    consumer.close()
    print()
    print()
    print("Done!")
    
    
if __name__ == "__main__":
    sentiment_analysis()
    print("Sentiment analysis completed.")