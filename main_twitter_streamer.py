import json
import string
from datetime import *

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from twitter_football_analysis import config, sentiment_juicer, pandas_juicer

auth = OAuthHandler(config.key, config.secret)
auth.set_access_token(config.token, config.token_secret)
api = tweepy.API(auth)

stop_words = set(stopwords.words("english"))
stop_words.update(set(list(string.punctuation) +['RT', 'https']))
sid = SentimentIntensityAnalyzer()


count = 0


def update_timer():
    global timer, neg_sent, pos_sent, count, pos_tweets, neg_tweets
    timer = datetime.now() + timedelta(seconds=10)
    if count > 0:
        data_explore(pos_sent, neg_sent, count, pos_tweets, neg_tweets)

    #reset variables
    neg_sent = 0
    pos_sent = 0
    count = 0
    neg_tweets = ""
    pos_tweets = ""
    return timer, neg_sent, pos_sent, count

update_timer()


class StreamTweets(StreamListener):
    def on_data(self, data):
        try:
            # clean tweet
            parsed_tweet = json.loads(data)
            tweet_text = parsed_tweet['text']
            break_tweet = word_tokenize(tweet_text)
            remove_stopwords = [word for word in break_tweet if not word in stop_words]
            cleaned_tweet = ' '.join(remove_stopwords)

            # NLTK stuffs
            sentiment_score = sid.polarity_scores(cleaned_tweet)
            for sent in sorted(sentiment_score):
                if (sent == 'neg' or sent == 'pos') and sentiment_score[sent] != 0.0:

                    global neg_sent, pos_sent, neg_tweets, pos_tweets
                    if sent == 'neg':
                        neg_sent += -sentiment_score[sent]
                        pos_tweets += ''.join(cleaned_tweet) + ' '
                    elif sent == 'pos':
                        pos_sent += sentiment_score[sent]
                        neg_tweets += ''.join(cleaned_tweet) + ' '


            global count
            count += 1
            if datetime.now() > timer:
                update_timer()
            return True

        except BaseException as e:
            print('error on data: %e' % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True


def data_explore(pos_sent ,neg_sent, count, pos_tweets, sent):
    sentiment_juicer.tweet_analyse(pos_tweets, 'pos')
    sentiment_juicer.tweet_analyse(neg_tweets, 'neg')
    pandas_juicer.twitter_sent_build_dicts(pos_sent, neg_sent, count)



twitter_stream = Stream(auth, StreamTweets())
twitter_stream.filter(track=['#brexit', 'brexit'])
