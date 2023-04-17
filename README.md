
# Analyze financial news with FinBERT

## Project description
This is an small application that showcases how to get financial news sentiment from Tiingo API and NLP pretrained models. 

* Download news from Tiingo API within the desired dates range for the selected tickers.
* Load the FinBERT pretrained model from Hugging Face model hub and use it to score each piece of news.
* Classify those news in positive, negative or neutral based on a simple heuristic.
* This feature could be used later on a bigger model to try to predict stocks direction.
* This app could be modified to store the news and sentiment into a database with the proper format.

## How to run it
* Clone the repository
* Install `pipenv` if needed: `pip install pipenv --user`.
* Install required libraries. Go to the cloned directory and run: `pipenv install` which will install dependencies based on my Pipfile.lock.
* You'll need your own Tiingo APIKEY. Create a `.env` file and write `TIINGO_APIKEY="your-key-here"`.
* Define tickers and dates of interest an just run it. 

<br>

# FinBERT: Financial Sentiment Analysis with BERT
FinBERT sentiment analysis model is available on Hugging Face model hub. [Check out their repo](https://github.com/PabloCanovas/finBERT)

FinBERT is a pre-trained NLP model to analyze sentiment of financial text. It is built by further training the BERT language model in the finance domain, using a large financial corpus and thereby fine-tuning it for financial sentiment classification. For the details, please see FinBERT: Financial Sentiment Analysis with Pre-trained Language Models.
