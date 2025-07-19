# Crypto News Sentiment Analysis

A real-time cryptocurrency news sentiment analysis system that fetches news from CryptoPanic API, streams it through Apache Kafka, and performs sentiment analysis using Hugging Face transformers.

## Features

- **News Fetching**: Retrieves latest Ethereum-focused news from CryptoPanic API
- **Real-time Streaming**: Uses Apache Kafka for reliable message streaming
- **Sentiment Analysis**: Analyzes news sentiment using pre-trained transformer models
- **Batch Processing**: Processes the last 20 messages for sentiment scoring
- **Overall Sentiment Score**: Calculates average sentiment across all analyzed messages

## Architecture

```
CryptoPanic API → Producer → Kafka Topic → Consumer → Sentiment Analysis → Results
```

## Prerequisites

- Python 3.7+
- Docker (for Kafka setup)
- CryptoPanic API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crypto-news-sentiment-analysis
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   CRYPTOPANIC_API_KEY=your_cryptopanic_api_key_here
   ```

4. **Start Kafka services**
   ```bash
   # Start Zookeeper
   sudo docker start kafka-zookeeper-1
   
   # Start Kafka
   sudo docker start kafka-kafka-1
   ```

## Required Dependencies

Add these to your `requirements.txt`:

```txt
requests
python-dotenv
kafka-python
transformers
torch
```

## Usage

### Quick Start

Run the complete pipeline:

```bash
python main.py
```

This will:
1. Fetch latest crypto news from CryptoPanic
2. Send news to Kafka topic
3. Perform sentiment analysis on the last 20 messages
4. Display individual and overall sentiment scores

### Individual Components

**Fetch and produce news only:**
```bash
python producer.py
```

**Analyze sentiment only:**
```bash
python sentiment_analysis.py
```

## Kafka Management

### Access Kafka CLI
```bash
sudo docker exec -it kafka-kafka-1 bash
```

### Create Topic
```bash
kafka-topics --create \
  --topic crypto-news \
  --partitions 1 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092
```

### Manual Message Production
```bash
kafka-console-producer --topic crypto-news --bootstrap-server localhost:9092
```

### Manual Message Consumption
```bash
kafka-console-consumer --topic crypto-news --from-beginning --bootstrap-server localhost:9092
```

## Configuration

### Producer Settings
- **Topic**: `crypto-news`
- **Bootstrap Servers**: `localhost:9092`
- **Currency Focus**: Ethereum (ETH)

### Consumer Settings
- **Messages Analyzed**: Last 20 messages
- **Sentiment Model**: Default Hugging Face sentiment-analysis pipeline
- **Scoring**: Positive sentiments add to score, negative sentiments subtract

### API Configuration
The system uses CryptoPanic's free API with the following endpoint:
```
https://cryptopanic.com/api/v1/posts/?auth_token={API_KEY}&currencies=ETH
```

## Output Format

The sentiment analysis provides:

1. **Individual Analysis**:
   ```
   Title: Bitcoin Reaches New Heights
   Sentiment: POSITIVE (score: 0.9245)
   ============================================================
   ```

2. **Overall Summary**:
   ```
   ############################################################
   Average sentiment score for the last 20 messages: 0.1234
   Overall sentiment is positive.
   ############################################################
   ```

## Project Structure

```
├── main.py                 # Main orchestration script
├── producer.py            # Kafka producer for news fetching
├── sentiment_analysis.py  # Sentiment analysis consumer
├── notes.md              # Development notes and commands
├── .env                  # Environment variables (create this)
└── README.md             # This file
```

## Error Handling

The system includes basic error handling for:
- Missing API keys
- Kafka connection issues
- Empty or malformed messages
- API rate limits

## Getting a CryptoPanic API Key

1. Visit [CryptoPanic](https://cryptopanic.com/developers/api/)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

## Limitations

- Currently focuses only on Ethereum news
- Processes a fixed number of last messages (20)
- Uses default sentiment analysis model (can be customized)
- Requires manual Kafka setup

## Future Enhancements

- Support for multiple cryptocurrencies
- Real-time streaming analysis
- Custom sentiment models
- Web dashboard for visualization
- Historical sentiment tracking
- Alert system for sentiment changes

## Troubleshooting

**Kafka not running**: Ensure Docker containers are started
**API key errors**: Verify your CryptoPanic API key in `.env`
**No messages**: Check if the topic exists and producer ran successfully
**Sentiment analysis slow**: First run downloads the transformer model

## License

This project is open source and available under the MIT License.