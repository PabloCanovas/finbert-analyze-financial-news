import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from utils.tiingo_client import MyTiingoClient
from utils.date_utils import *


class TiingoNewsAnalyzer:

    def __init__(self):
        self.tiingo_client = MyTiingoClient().get_client()
        self.model_name = "ProsusAI/finbert" 
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def get_tiingo_news(self, source_list, start_date, end_date, tickers, limit = 10):
        """Download the news into a nice dataframe"""
        
        try:
            response = self.tiingo_client.get_news(sources = source_list,
                                                    startDate = str(start_date),
                                                    endDate = str(end_date),
                                                    tickers = tickers,
                                                    limit = limit)
            news_df = pd.DataFrame(response)
            news_df['publishedDate'] = news_df['publishedDate'].apply(lambda x: parse_tiingo_date(x))

            return news_df
        
        except Exception:
            return print("Error while retrieving news from Tiingo!")


    def get_news_sentiment(self, news_df):
        """Receives a news dataframe and use pretrained FinBert model to classify news sentiment"""

        for i, r in news_df.iterrows():

            title = r["title"]
            description = r["description"]

            if not title or not description: continue

            content = title + ' ' + description

            inputs = self.tokenizer(content, padding=True, truncation=True, return_tensors='pt')
            outputs = self.model(**inputs)

            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            news_df.loc[i, 'sentiment_positive'] = predictions[0].tolist()[0]
            news_df.loc[i, 'sentiment_negative'] = predictions[0].tolist()[1]
            news_df.loc[i, 'sentiment_neutral'] = predictions[0].tolist()[2]
        
        news_df['sentiment_score'] = news_df['sentiment_positive'] - news_df['sentiment_negative']

        # define thresholds for neutral, positive, and negative sentiment
        neutral_threshold = 0.1
        positive_threshold = 0.3
        negative_threshold = -0.3

        # classify the sentiment based on the score and thresholds
        news_df['sentiment'] = 'Neutral'
        news_df['sentiment'] = np.where(news_df['sentiment_score'] >= positive_threshold, 'Positive', news_df['sentiment'])
        news_df['sentiment'] = np.where(news_df['sentiment_score'] <= negative_threshold, 'Negative', news_df['sentiment'])
        news_df['sentiment'] = np.where(abs(news_df['sentiment_score']) <= neutral_threshold, 'Neutral', news_df['sentiment'])

        return news_df


if __name__ == "__main__":
    tiingo = TiingoNewsAnalyzer()

    sources = ['reuters.com', 'finance.yahoo.com', 'marketwatch.com', 'bloomberg.com', 'investorplace.com']
    start_date = '2023-04-01'
    end_date = '2023-04-17'
    tickers = None
    limit = 10

    news_df = tiingo.get_tiingo_news(sources, start_date, end_date, tickers, limit)
    sentiment_df = tiingo.get_news_sentiment(news_df)

    for i, r in sentiment_df.iterrows():
        print(i+1, r['title'])
        print(r['description'])
        print(f"{r['sentiment']}: {round(r['sentiment_score'],2)}")
        print("\n")